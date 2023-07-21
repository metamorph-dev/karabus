from typing import AsyncGenerator
from typing import Generator

import alembic
import pytest
import pytest_asyncio
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import SessionTransaction

from app.db.session import get_session
from app.main import app as main_app
from app.settings import settings


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker(pytest.mark.asyncio)


@pytest_asyncio.fixture
def app():
    return main_app


@pytest_asyncio.fixture
async def ac(app) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="https://test") as c:
        yield c


def setup_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option('sqlalchemy.url', f"{settings.TEST_DB_URL}/test")
    alembic.command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session", autouse=True)
def setup_db() -> Generator:
    engine = create_engine(f"{settings.TEST_DB_URL}")
    conn = engine.connect()
    conn = conn.execution_options(isolation_level="AUTOCOMMIT")
    try:
        conn.execute(text("drop database test"))
    except SQLAlchemyError:
        pass
    finally:
        conn.close()

    conn = engine.connect()
    conn = conn.execution_options(isolation_level="AUTOCOMMIT")
    conn.execute(text("create database test"))
    setup_migrations()
    conn.close()

    yield

    conn = engine.connect()
    conn = conn.execution_options(isolation_level="AUTOCOMMIT")
    try:
        conn.execute(text("drop database test"))
    except SQLAlchemyError:
        pass
    conn.close()


@pytest_asyncio.fixture(scope="function")
async def session(app) -> AsyncGenerator:
    # https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    async_engine = create_async_engine(f"{settings.TEST_DB_URL}/test")
    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()
        AsyncSessionLocal = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
            future=True,
        )

        async_session = AsyncSessionLocal()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session_: Session, transaction_: SessionTransaction) -> None:
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                if conn.sync_connection:
                    conn.sync_connection.begin_nested()

        def test_get_session() -> Generator:
            try:
                yield AsyncSessionLocal
            except SQLAlchemyError:
                pass

        app.dependency_overrides[get_session] = test_get_session

        yield async_session
        await async_session.close()
        await conn.rollback()

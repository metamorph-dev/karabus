import logging
from typing import Annotated
from typing import AsyncIterator

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from app.settings import settings


logger = logging.getLogger(__name__)

async_engine = create_async_engine(settings.DB_URL, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(async_engine, autoflush=False)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as exc:
        logger.exception(exc)


AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]

from collections.abc import AsyncIterator
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.exceptions import NotFoundError
from app.models.base import Base


T = TypeVar("T", bound=Base)


async def read_all(session: AsyncSession, model: type[T]) -> AsyncIterator[T]:
    query = select(model).order_by(model.id.desc())
    stream = await session.stream_scalars(query)
    async for row in stream:
        yield row


async def read_by_id(session: AsyncSession, model: type[T], instance_id: int) -> T | None:
    query = select(model).where(model.id == instance_id)

    result = await session.scalar(query)
    if not result:
        raise NotFoundError()

    return result


async def delete(session: AsyncSession, instance: T) -> None:
    await session.delete(instance)
    await session.flush()

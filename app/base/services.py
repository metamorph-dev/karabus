from typing import AsyncIterator
from typing import Type
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.exceptions import NotFoundError
from app.base.models import Base


T = TypeVar("T", bound=Base)


async def read_all(session: AsyncSession, model: Type[T]) -> AsyncIterator[T]:
    query = (
        select(model)
        .order_by(model.id.desc())
    )
    stream = await session.stream_scalars(query)
    async for row in stream:
        yield row


async def read_by_id(session: AsyncSession, model: Type[T], instance_id: int) -> T | None:
    query = (
        select(model)
        .where(model.id == instance_id)
        .order_by(model.id)
    )

    if not (result := await session.scalar(query)):
        raise NotFoundError()

    return result


async def delete(session: AsyncSession, instance: T) -> None:
    await session.delete(instance)
    await session.flush()

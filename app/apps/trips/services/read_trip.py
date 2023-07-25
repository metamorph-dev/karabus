from collections.abc import AsyncIterator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload

from app.base.exceptions import NotFoundError
from app.models import Trip


async def read_trip(session: AsyncSession, instance_id: int) -> Trip:
    query = select(Trip).options(joinedload(Trip.bus), selectinload(Trip.stops)).where(Trip.id == instance_id)
    trip = await session.scalar(query)
    if not trip:
        raise NotFoundError(f"There is no trip with id {instance_id}")

    return trip


async def read_all_trips(session: AsyncSession, offset: int = 0, limit: int = 50) -> AsyncIterator[Trip]:
    query = select(Trip).options(joinedload(Trip.bus), selectinload(Trip.stops)).offset(offset).limit(limit)
    stream = await session.stream_scalars(query)
    async for row in stream:
        yield row

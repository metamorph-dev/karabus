from collections.abc import AsyncIterator

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import Order


async def read_orders(session, offset: int = 0, limit: int = 50) -> AsyncIterator[Order]:
    query = select(Order).options(selectinload(Order.passengers)).offset(offset).limit(limit).order_by(Order.id.desc())
    stream = await session.stream_scalars(query)
    async for row in stream:
        yield row

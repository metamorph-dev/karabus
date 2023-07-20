from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.base.exceptions import NotFoundError
from app.models import Order


async def read_order_by_id(session: AsyncSession, order_id: int) -> Order:
    query = (
        select(Order)
        .options(joinedload(Order.passengers))
        .where(Order.id == order_id)
    )
    order = await session.scalar(query)

    if not order:
        raise NotFoundError(f"There is no order with id {order_id}")

    return order

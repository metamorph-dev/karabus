from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.orders.enums import OrderStatus
from app.models import Order


async def update_order_status(session: AsyncSession, order: Order, status: OrderStatus) -> None:
    order.status = status
    await session.flush()

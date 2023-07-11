from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.busses.models import Bus


async def read_bus_by_number_plate(session: AsyncSession, number_plate: str) -> Bus | None:
    query = (
        select(Bus)
        .where(Bus.number_plate == number_plate)
        .order_by(Bus.id)
    )
    return await session.scalar(query)

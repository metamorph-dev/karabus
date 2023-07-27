from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Bus
from app.models import Trip


async def update_trip(  # noqa: PLR0913
    session: AsyncSession,
    trip: Trip,
    name: str,
    price: int,
    bus: Bus,
    seats_left: int,
) -> None:
    trip.name = name
    trip.price = price
    trip.bus = bus
    trip.seats_left = seats_left

    await session.flush()

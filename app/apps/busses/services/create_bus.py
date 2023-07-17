from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.busses.enums import Color
from app.base.exceptions import AlreadyExistError
from app.models import Bus


async def create_bus(
    session: AsyncSession,
    color: Color,
    seats_quantity: int,
    number_plate: str,
) -> Bus:
    bus = Bus(color=color, seats_quantity=seats_quantity, number_plate=number_plate)
    session.add(bus)

    try:
        await session.flush()
    except IntegrityError as exc:
        raise AlreadyExistError(f"The bus with number plate {number_plate} already exists") from exc

    return bus

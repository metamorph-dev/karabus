from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.busses.enums import Color
from app.base.exceptions import AlreadyExistError
from app.models import Bus


async def update_bus(
    session: AsyncSession,
    bus: Bus,
    color: Color,
    seats_quantity: int,
    number_plate: str,
) -> None:
    bus.color = color
    bus.seats_quantity = seats_quantity
    bus.number_plate = number_plate

    try:
        await session.flush()
    except IntegrityError as exc:
        raise AlreadyExistError(f"The bus with number plate {number_plate} already exists") from exc

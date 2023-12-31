from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.exceptions import AlreadyExistError
from app.models import City


async def create_city(
    session: AsyncSession,
    name: str,
    longitude: float,
    latitude: float,
) -> City:
    city = City(name=name, longitude=longitude, latitude=latitude)
    session.add(city)

    try:
        await session.flush()
    except IntegrityError as exc:
        raise AlreadyExistError(f"The city with name {name} already exists") from exc

    return city

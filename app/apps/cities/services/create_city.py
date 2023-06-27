from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.cities.models import City
from app.base.exceptions import AlreadyExistError


async def create_city(
        session: AsyncSession,
        name: str,
        longitude: float,
        latitude: float,
) -> City:
    session.add(city := City(name=name, longitude=longitude, latitude=latitude))

    try:
        await session.flush()
    except IntegrityError as exc:
        raise AlreadyExistError(f"The city with name {name} already exists") from exc

    return city

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.cities.models import City
from app.base.exceptions import AlreadyExistError


async def update_city(
        session: AsyncSession,
        city: City,
        name: str,
        longitude: float,
        latitude: float,
) -> None:
    city.name = name
    city.longitude = longitude
    city.latitude = latitude

    try:
        await session.flush()
    except IntegrityError as exc:
        raise AlreadyExistError(f"The city with name {name} already exists") from exc

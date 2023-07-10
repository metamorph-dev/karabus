from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.cities.models import City


async def read_city_by_name(session: AsyncSession, name: str) -> City | None:
    query = (
        select(City)
        .where(City.name == name)
        .order_by(City.id)
    )
    return await session.scalar(query)

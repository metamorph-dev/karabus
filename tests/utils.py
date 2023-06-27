from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.cities.models import City


def clean_response_data(response_data: dict) -> dict:
    del response_data["id"]
    del response_data["created_at"]
    del response_data["updated_at"]
    return response_data


async def create_test_cities(session: AsyncSession, count: int = 1) -> None:
    session.add_all([
        City(name=f"City-{i}", longitude=i, latitude=i)
        for i in range(1, count + 1)
    ])
    await session.flush()
    await session.commit()

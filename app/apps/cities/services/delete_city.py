from typing import Annotated

from fastapi import Depends

from app.apps.cities.repositories import CityRepository
from app.db.session import AsyncSession


class DeleteCityLocal:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def execute(self, city_id: int) -> None:
        async with self.session.begin() as session:
            repository = CityRepository(session)
            city = await repository.read(city_id)
            await repository.delete(city)


DeleteCity = Annotated[DeleteCityLocal, Depends()]

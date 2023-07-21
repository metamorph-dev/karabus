from typing import Annotated

from fastapi import Depends

from app.apps.cities.repositories import CityRepository
from app.apps.cities.schemas.read_city_response import ReadCityResponse
from app.db.session import AsyncSession


class ReadCityLocal:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def execute(self, city_id: int) -> ReadCityResponse:
        async with self.session.begin() as session:
            repository = CityRepository(session)
            city = await repository.read(city_id)
            return ReadCityResponse.model_validate(city)


ReadCity = Annotated[ReadCityLocal, Depends()]

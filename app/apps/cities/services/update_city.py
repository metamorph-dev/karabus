from typing import Annotated

from fastapi import Depends

from app.apps.cities.repositories import CityRepository
from app.apps.cities.schemas.udpate_city_request import UpdateCityRequest
from app.apps.cities.schemas.update_city_response import UpdateCityResponse
from app.db.session import AsyncSession


class UpdateCityLocal:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def execute(self, city_id: int, schema: UpdateCityRequest) -> UpdateCityResponse:
        async with self.session.begin() as session:
            repository = CityRepository(session)
            city = await repository.read(city_id)
            await repository.update(city, schema)
            await session.refresh(city)
            return UpdateCityResponse.model_validate(city)


UpdateCity = Annotated[UpdateCityLocal, Depends()]

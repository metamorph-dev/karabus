from typing import Annotated

from fastapi import Depends

from app.apps.cities.repositories import CityRepository
from app.apps.cities.schemas.create_city_request import CreateCityRequest
from app.apps.cities.schemas.create_city_response import CreateCityResponse
from app.db.session import AsyncSession


class CreateCityLocal:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def execute(self, schema: CreateCityRequest) -> CreateCityResponse:
        async with self.session.begin() as session:
            repository = CityRepository(session)
            city = await repository.create(schema)
            return CreateCityResponse.model_validate(city)


CreateCity = Annotated[CreateCityLocal, Depends()]

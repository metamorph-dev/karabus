from typing import Annotated
from typing import AsyncIterator

from fastapi import Depends

from app.apps.cities.repositories import CityRepository
from app.apps.cities.schemas.read_cities_request import ReadCitiesRequest
from app.apps.cities.schemas.read_city_response import ReadCityResponse
from app.db.session import AsyncSession


class ReadCitiesLocal:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def execute(self, schema: ReadCitiesRequest) -> AsyncIterator[ReadCityResponse]:
        async with self.session.begin() as session:
            repository = CityRepository(session)
            async for bus in repository.read_page(schema):
                yield ReadCityResponse.model_validate(bus)


ReadCities = Annotated[ReadCitiesLocal, Depends()]

from typing import AsyncIterator

from app.apps.cities.models import City
from app.apps.cities.schemas import CitySchema
from app.apps.cities.schemas import CreateCityResponse
from app.apps.cities.schemas import ReadCityResponse
from app.apps.cities.schemas import UpdateCityResponse
from app.apps.cities.services.create_city import create_city
from app.apps.cities.services.update_city import update_city
from app.base.services import delete
from app.base.services import read_all
from app.base.services import read_by_id
from app.db import AsyncSession


class CreateCity:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, name: str, longitude: float, latitude: float) -> CreateCityResponse:
        async with self.async_session.begin() as session:
            city = await create_city(session, name, longitude, latitude)
            return CreateCityResponse.from_orm(city)


class ReadCity:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, city_id: int) -> ReadCityResponse:
        async with self.async_session.begin() as session:
            city = await read_by_id(session, City, city_id)
            return ReadCityResponse.from_orm(city)


class ReadAllCities:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self) -> AsyncIterator[CitySchema]:
        async with self.async_session.begin() as session:
            async for city in read_all(session, City):
                yield CitySchema.from_orm(city)


class UpdateCity:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, city_id: int, name: str, longitude: float, latitude: float) -> UpdateCityResponse:
        async with self.async_session.begin() as session:
            city = await read_by_id(session, City, city_id)
            await update_city(session, city, name, longitude, latitude)
            await session.refresh(city)
            return UpdateCityResponse.from_orm(city)


class DeleteCity:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, city_id: int) -> None:
        async with self.async_session.begin() as session:
            await delete(session, await read_by_id(session, City, city_id))

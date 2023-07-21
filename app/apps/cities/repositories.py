from typing import AsyncIterator

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.cities.exceptions.already_exists import CityAlreadyExistsException
from app.apps.cities.exceptions.not_found import CityNotFoundException
from app.apps.cities.schemas.create_city_request import CreateCityRequest
from app.apps.cities.schemas.read_cities_request import ReadCitiesRequest
from app.apps.cities.schemas.udpate_city_request import UpdateCityRequest
from app.models import City


class CityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, schema: CreateCityRequest) -> City:
        city = City(**schema.model_dump())
        self.session.add(city)

        try:
            await self.session.flush()
        except IntegrityError as exc:
            raise CityAlreadyExistsException(schema.name) from exc

        return city

    async def read_page(self, schema: ReadCitiesRequest) -> AsyncIterator[City]:
        query = (
            select(City)
            .order_by(City.id.desc())
            .offset(schema.offset)
            .limit(schema.limit)
        )
        stream = await self.session.stream_scalars(query)
        async for row in stream:
            yield row

    async def read(self, city_id: int) -> City:
        query = (
            select(City)
            .where(City.id == city_id)
        )
        city = await self.session.scalar(query)
        if not city:
            raise CityNotFoundException(city_id)
        return city

    async def update(self, city: City, schema: UpdateCityRequest) -> None:
        for key, value in schema.model_dump(exclude_unset=True).items():
            setattr(city, key, value)

        try:
            await self.session.flush()
        except IntegrityError as exc:
            raise CityAlreadyExistsException(schema.name) from exc

    async def delete(self, city: City) -> None:
        await self.session.delete(city)
        await self.session.flush()

from typing import AsyncIterator

from sqlalchemy.exc import InvalidRequestError

from app.apps.trips.schemas import CreateTripRequest
from app.apps.trips.schemas import CreateTripResponse
from app.apps.trips.schemas import ReadTripResponse
from app.apps.trips.schemas import TripSchema
from app.apps.trips.schemas import UpdateTripResponse
from app.apps.trips.services.create_trip import create_trip
from app.apps.trips.services.read_trip import read_all_trips
from app.apps.trips.services.read_trip import read_trip
from app.apps.trips.services.update_trip import update_trip
from app.base.exceptions import NotFoundError
from app.base.services import delete
from app.base.services import read_by_id
from app.db import AsyncSession
from app.models import Bus
from app.models import Trip


class CreateTrip:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, data: CreateTripRequest) -> CreateTripResponse:
        async with self.async_session.begin() as session:
            session: AsyncSession

            try:
                bus = await read_by_id(session, Bus, data.bus_id)
            except NotFoundError as exc:
                raise NotFoundError(f"There is no bus with id {data.bus_id}") from exc

            trip = await create_trip(session, bus, data)

            try:
                result = CreateTripResponse.from_orm(trip)
            except InvalidRequestError as exc:
                raise NotFoundError("There is no cities with such id(s)") from exc

            return result


class ReadAllTrip:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, offset: int = 0, limit: int = 50) -> AsyncIterator[TripSchema]:
        async with self.async_session.begin() as session:
            async for trip in read_all_trips(session, offset, limit):
                yield TripSchema.from_orm(trip)


class ReadTrip:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, trip_id: int) -> ReadTripResponse:
        async with self.async_session.begin() as session:
            trip = await read_trip(session, trip_id)
            return ReadTripResponse.from_orm(trip)


class UpdateTrip:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(
        self,
        trip_id: int,
        bus_id: int,
        name: str,
        price: int,
        seats_left: int,
    ) -> UpdateTripResponse:
        async with self.async_session.begin() as session:
            try:
                trip = await read_by_id(session, Trip, trip_id)
            except NotFoundError as exc:
                raise NotFoundError(f"There is no trip with id {trip_id}") from exc

            try:
                bus = await read_by_id(session, Bus, bus_id)
            except NotFoundError as exc:
                raise NotFoundError(f"There is no bus with id {bus_id}") from exc

            await update_trip(session, trip, name, price, bus, seats_left)
            await session.refresh(trip)

            trip = await read_trip(session, trip.id)
            return UpdateTripResponse.from_orm(trip)


class DeleteTrip:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, trip_id: int) -> None:
        async with self.async_session.begin() as session:
            trip = await read_by_id(session, Trip, trip_id)
            await delete(session, trip)

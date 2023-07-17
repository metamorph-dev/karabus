from typing import AsyncIterator

from app.apps.busses.enums import Color
from app.apps.busses.schemas import BusSchema
from app.apps.busses.schemas import CreateBusResponse
from app.apps.busses.schemas import ReadBusResponse
from app.apps.busses.schemas import UpdateBusResponse
from app.apps.busses.services.create_bus import create_bus
from app.apps.busses.services.update_bus import update_bus
from app.base.services import delete
from app.base.services import read_all
from app.base.services import read_by_id
from app.db import AsyncSession
from app.models import Bus


class CreateBus:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, color: Color, seats_quantity: int, number_plate: str) -> CreateBusResponse:
        async with self.async_session.begin() as session:
            bus = await create_bus(session, color, seats_quantity, number_plate)
            return CreateBusResponse.from_orm(bus)


class ReadBus:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, bus_id: int) -> ReadBusResponse:
        async with self.async_session.begin() as session:
            bus = await read_by_id(session, Bus, bus_id)
            return ReadBusResponse.from_orm(bus)


class ReadAllBusses:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self) -> AsyncIterator[BusSchema]:
        async with self.async_session.begin() as session:
            async for bus in read_all(session, Bus):
                yield BusSchema.from_orm(bus)


class UpdateBus:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, bus_id: int, color: Color, seats_quantity: int, number_plate: str) -> UpdateBusResponse:
        async with self.async_session.begin() as session:
            bus = await read_by_id(session, Bus, bus_id)
            await update_bus(session, bus, color, seats_quantity, number_plate)
            await session.refresh(bus)
            return UpdateBusResponse.from_orm(bus)


class DeleteBus:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, bus_id: int) -> None:
        async with self.async_session.begin() as session:
            bus = await read_by_id(session, Bus, bus_id)
            await delete(session, bus)

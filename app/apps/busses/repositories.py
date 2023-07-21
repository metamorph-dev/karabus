from typing import AsyncIterator

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.busses.exceptions.already_exists import BusAlreadyExistsException
from app.apps.busses.exceptions.not_found import BusNotFoundException
from app.apps.busses.schemas.create_bus_request import CreateBusRequest
from app.apps.busses.schemas.read_busses_request import ReadBussesRequest
from app.apps.busses.schemas.update_bus_request import UpdateBusRequest
from app.models import Bus


class BusRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, schema: CreateBusRequest) -> Bus:
        bus = Bus(**schema.model_dump())
        self.session.add(bus)

        try:
            await self.session.flush()
        except IntegrityError as exc:
            raise BusAlreadyExistsException(schema.number_plate) from exc

        return bus

    async def read_page(self, schema: ReadBussesRequest) -> AsyncIterator[Bus]:
        query = (
            select(Bus)
            .order_by(Bus.id.desc())
            .offset(schema.offset)
            .limit(schema.limit)
        )
        stream = await self.session.stream_scalars(query)
        async for row in stream:
            yield row

    async def read(self, bus_id: int) -> Bus:
        query = (
            select(Bus)
            .where(Bus.id == bus_id)
        )
        bus = await self.session.scalar(query)
        if not bus:
            raise BusNotFoundException(bus_id)
        return bus

    async def update(self, bus: Bus, schema: UpdateBusRequest) -> None:
        for key, value in schema.model_dump(exclude_unset=True).items():
            setattr(bus, key, value)

        try:
            await self.session.flush()
        except IntegrityError as exc:
            raise BusAlreadyExistsException(schema.number_plate) from exc

    async def delete(self, bus: Bus) -> None:
        await self.session.delete(bus)
        await self.session.flush()

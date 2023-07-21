from typing import Annotated

from fastapi import Depends

from app.apps.busses.repositories import BusRepository
from app.apps.busses.schemas.read_bus_response import ReadBusResponse
from app.db.session import AsyncSession


class ReadBusLocal:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def execute(self, bus_id: int) -> ReadBusResponse:
        async with self.session.begin() as session:
            repository = BusRepository(session)
            bus = await repository.read(bus_id)
            return ReadBusResponse.model_validate(bus)


ReadBus = Annotated[ReadBusLocal, Depends()]

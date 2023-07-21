from typing import Annotated

from fastapi import Depends

from app.apps.busses.repositories import BusRepository
from app.apps.busses.schemas.update_bus_request import UpdateBusRequest
from app.apps.busses.schemas.update_bus_response import UpdateBusResponse
from app.db.session import AsyncSession


class UpdateBusLocal:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def execute(self, bus_id: int, schema: UpdateBusRequest) -> UpdateBusResponse:
        async with self.session.begin() as session:
            repository = BusRepository(session)
            bus = await repository.read(bus_id)
            await repository.update(bus, schema)
            await session.refresh(bus)
            return UpdateBusResponse.model_validate(bus)


UpdateBus = Annotated[UpdateBusLocal, Depends()]

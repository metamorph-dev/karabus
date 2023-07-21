from typing import Annotated

from fastapi import Depends

from app.apps.busses.repositories import BusRepository
from app.apps.busses.schemas.create_bus_request import CreateBusRequest
from app.apps.busses.schemas.create_bus_response import CreateBusResponse
from app.db.session import AsyncSession


class CreateBusLocal:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def execute(self, schema: CreateBusRequest) -> CreateBusResponse:
        async with self.session.begin() as session:
            repository = BusRepository(session)
            bus = await repository.create(schema)
            return CreateBusResponse.model_validate(bus)


CreateBus = Annotated[CreateBusLocal, Depends()]

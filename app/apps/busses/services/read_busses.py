from typing import Annotated
from typing import AsyncIterator

from fastapi import Depends

from app.apps.busses.repositories import BusRepository
from app.apps.busses.schemas.read_bus_response import ReadBusResponse
from app.apps.busses.schemas.read_busses_request import ReadBussesRequest
from app.db.session import AsyncSession


class ReadBussesLocal:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def execute(self, schema: ReadBussesRequest) -> AsyncIterator[ReadBusResponse]:
        async with self.session.begin() as session:
            repository = BusRepository(session)
            async for bus in repository.read_page(schema):
                yield ReadBusResponse.model_validate(bus)


ReadBusses = Annotated[ReadBussesLocal, Depends()]

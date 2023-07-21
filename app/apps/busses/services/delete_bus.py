from typing import Annotated

from fastapi import Depends

from app.apps.busses.repositories import BusRepository
from app.db.session import AsyncSession


class DeleteBusLocal:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def execute(self, bus_id: int) -> None:
        async with self.session.begin() as session:
            repository = BusRepository(session)
            bus = await repository.read(bus_id)
            await repository.delete(bus)


DeleteBus = Annotated[DeleteBusLocal, Depends()]

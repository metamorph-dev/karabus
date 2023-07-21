from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from app.apps.busses.schemas.create_bus_request import CreateBusRequest
from app.apps.busses.schemas.create_bus_response import CreateBusResponse
from app.apps.busses.schemas.read_bus_response import ReadBusResponse
from app.apps.busses.schemas.read_busses_request import ReadBussesRequest
from app.apps.busses.schemas.read_busses_response import ReadBussesResponse
from app.apps.busses.schemas.update_bus_request import UpdateBusRequest
from app.apps.busses.schemas.update_bus_response import UpdateBusResponse
from app.apps.busses.services.create_bus import CreateBus
from app.apps.busses.services.delete_bus import DeleteBus
from app.apps.busses.services.read_bus import ReadBus
from app.apps.busses.services.read_busses import ReadBusses
from app.apps.busses.services.update_bus import UpdateBus


busses_router = APIRouter(prefix="/busses", tags=["busses"])
router = busses_router


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_bus(service: CreateBus, schema: CreateBusRequest) -> CreateBusResponse:
    return await service.execute(schema)


@router.get("/{bus_id}")
async def read_bus(bus_id: int, service: ReadBus) -> ReadBusResponse:
    return await service.execute(bus_id)


@router.get("/")
async def read_busses(service: ReadBusses, schema: ReadBussesRequest = Depends()) -> ReadBussesResponse:
    return ReadBussesResponse(busses=[bus async for bus in service.execute(schema)])


@router.patch("/{bus_id}")
async def update_bus(bus_id: int, service: UpdateBus, schema: UpdateBusRequest) -> UpdateBusResponse:
    return await service.execute(bus_id, schema)


@router.delete("/{bus_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bus(bus_id: int, service: DeleteBus) -> None:
    return await service.execute(bus_id)

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.params import Path

from app.apps.busses.schemas import CreateBusRequest
from app.apps.busses.schemas import CreateBusResponse
from app.apps.busses.schemas import ReadAllBusResponse
from app.apps.busses.schemas import ReadBusResponse
from app.apps.busses.schemas import UpdateBusRequest
from app.apps.busses.schemas import UpdateBusResponse
from app.apps.busses.use_cases import CreateBus
from app.apps.busses.use_cases import DeleteBus
from app.apps.busses.use_cases import ReadAllBusses
from app.apps.busses.use_cases import ReadBus
from app.apps.busses.use_cases import UpdateBus
from app.base.exceptions import AlreadyExistError
from app.base.exceptions import NotFoundError


router = APIRouter(prefix="/busses", tags=["busses"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(data: CreateBusRequest, use_case: CreateBus = Depends()) -> CreateBusResponse:
    try:
        result = await use_case.execute(data.color, data.seats_quantity, data.number_plate)
    except AlreadyExistError as exc:
        raise HTTPException(400, str(exc))

    return result


@router.get("/{bus_id}")
async def read(bus_id: int = Path(...), use_case: ReadBus = Depends()) -> ReadBusResponse:
    try:
        result = await use_case.execute(bus_id)
    except NotFoundError:
        raise HTTPException(404, "Not found")

    return result


@router.get("/")
async def read_all(use_case: ReadAllBusses = Depends()) -> ReadAllBusResponse:
    return ReadAllBusResponse(busses=[bus async for bus in use_case.execute()])


@router.put("/{bus_id}")
async def update(
    data: UpdateBusRequest,
    bus_id: int = Path(...),
    use_case: UpdateBus = Depends(),
) -> UpdateBusResponse:
    try:
        result = await use_case.execute(bus_id, data.color, data.seats_quantity, data.number_plate)
    except NotFoundError:
        raise HTTPException(404, "Not found")
    except AlreadyExistError as exc:
        raise HTTPException(400, str(exc))

    return result


@router.delete("/{bus_id}", status_code=204)
async def delete(bus_id: int = Path(...), use_case: DeleteBus = Depends()) -> None:
    try:
        await use_case.execute(bus_id)
    except NotFoundError:
        pass

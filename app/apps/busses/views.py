import contextlib
import pathlib
import uuid

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status
from fastapi.params import Path

from app.apps.busses.constants import MAX_FILENAME_SUFFIX_LENGTH
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
from app.base.services import read_by_id
from app.db import AsyncSession
from app.models import Bus


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


@router.put("/{bus_id}/photo")
async def upload_bus_photo(bus_id: int, async_session: AsyncSession, file: UploadFile = File(...)) -> ReadBusResponse:
    suffix = pathlib.Path(file.filename).suffix
    if len(suffix) > MAX_FILENAME_SUFFIX_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Filename suffix length is bigger than {MAX_FILENAME_SUFFIX_LENGTH}",
        )

    static = pathlib.Path("static")
    new_filename = str(uuid.uuid4()) + suffix
    data = file.file.read()

    file_path = static / new_filename
    with file_path.open("wb") as new_file:
        new_file.write(data)

    async with async_session.begin() as session:
        try:
            bus = await read_by_id(session, Bus, bus_id)
        except NotFoundError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"There is no bus with id {bus_id}")

        bus.photo_filename = new_filename
        await session.flush()
        return ReadBusResponse.from_orm(bus)


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
    with contextlib.suppress(NotFoundError):
        await use_case.execute(bus_id)

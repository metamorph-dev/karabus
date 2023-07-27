import contextlib

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from fastapi import status

from app.apps.trips.schemas import CreateTripRequest
from app.apps.trips.schemas import CreateTripResponse
from app.apps.trips.schemas import ReadAllTripResponse
from app.apps.trips.schemas import ReadTripResponse
from app.apps.trips.schemas import UpdateTripRequest
from app.apps.trips.schemas import UpdateTripResponse
from app.apps.trips.use_cases import CreateTrip
from app.apps.trips.use_cases import DeleteTrip
from app.apps.trips.use_cases import ReadAllTrip
from app.apps.trips.use_cases import ReadTrip
from app.apps.trips.use_cases import UpdateTrip
from app.base.exceptions import NotFoundError


router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    data: CreateTripRequest,
    use_case: CreateTrip = Depends(),
) -> CreateTripResponse:
    try:
        result = await use_case.execute(data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc))

    return result


@router.get("/{trip_id}")
async def read(trip_id: int, use_case: ReadTrip = Depends()) -> ReadTripResponse:
    try:
        result = await use_case.execute(trip_id)
    except NotFoundError:
        raise HTTPException(404, "Not Found")
    return result


@router.get("/")
async def read_all(use_case: ReadAllTrip = Depends(), offset: int = 0, limit: int = 50) -> ReadAllTripResponse:
    return ReadAllTripResponse(trips=[trip async for trip in use_case.execute(offset, limit)])


@router.put("/{trip_id}")
async def update(
    data: UpdateTripRequest,
    trip_id: int = Path(...),
    use_case: UpdateTrip = Depends(),
) -> UpdateTripResponse:
    try:
        result = await use_case.execute(trip_id, data.bus_id, data.name, data.price, data.seats_left)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc

    return result


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(trip_id: int = Path(...), use_case: DeleteTrip = Depends()) -> None:
    with contextlib.suppress(NotFoundError):
        await use_case.execute(trip_id)

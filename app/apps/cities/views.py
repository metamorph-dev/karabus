from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from fastapi import status

from app.apps.cities.schemas import CreateCityRequest
from app.apps.cities.schemas import CreateCityResponse
from app.apps.cities.schemas import ReadAllCitiesResponse
from app.apps.cities.schemas import ReadCityResponse
from app.apps.cities.schemas import UpdateCityRequest
from app.apps.cities.schemas import UpdateCityResponse
from app.apps.cities.use_cases import CreateCity
from app.apps.cities.use_cases import DeleteCity
from app.apps.cities.use_cases import ReadAllCities
from app.apps.cities.use_cases import ReadCity
from app.apps.cities.use_cases import UpdateCity
from app.base.exceptions import AlreadyExistError
from app.base.exceptions import NotFoundError


router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    data: CreateCityRequest,
    use_case: CreateCity = Depends(),
) -> CreateCityResponse:
    try:
        result = await use_case.execute(data.name, data.longitude, data.latitude)
    except AlreadyExistError as exc:
        raise HTTPException(400, str(exc))
    return result


@router.get("/{city_id}")
async def read(
    city_id: int = Path(...),
    use_case: ReadCity = Depends(),
) -> ReadCityResponse:
    try:
        result = await use_case.execute(city_id)
    except NotFoundError:
        raise HTTPException(404, "Not found")
    return result


@router.get("/")
async def read_all(use_case: ReadAllCities = Depends()) -> ReadAllCitiesResponse:
    return ReadAllCitiesResponse(cities=[city async for city in use_case.execute()])


@router.put("/{city_id}")
async def update(
    data: UpdateCityRequest,
    city_id: int = Path(...),
    use_case: UpdateCity = Depends(),
) -> UpdateCityResponse:
    try:
        result = await use_case.execute(city_id, data.name, data.longitude, data.latitude)
    except NotFoundError:
        raise HTTPException(404, "Not found")
    except AlreadyExistError as exc:
        raise HTTPException(400, str(exc))

    return result


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(city_id: int = Path(...), use_case: DeleteCity = Depends()) -> None:
    try:
        await use_case.execute(city_id)
    except NotFoundError:
        pass

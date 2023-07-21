from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from app.apps.cities.schemas.create_city_request import CreateCityRequest
from app.apps.cities.schemas.create_city_response import CreateCityResponse
from app.apps.cities.schemas.read_cities_request import ReadCitiesRequest
from app.apps.cities.schemas.read_cities_response import ReadCitiesResponse
from app.apps.cities.schemas.read_city_response import ReadCityResponse
from app.apps.cities.schemas.udpate_city_request import UpdateCityRequest
from app.apps.cities.schemas.update_city_response import UpdateCityResponse
from app.apps.cities.services.create_city import CreateCity
from app.apps.cities.services.delete_city import DeleteCity
from app.apps.cities.services.read_cities import ReadCities
from app.apps.cities.services.read_city import ReadCity
from app.apps.cities.services.update_city import UpdateCity


cities_router = APIRouter(prefix="/cities", tags=["cities"])
router = cities_router


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_city(service: CreateCity, schema: CreateCityRequest) -> CreateCityResponse:
    return await service.execute(schema)


@router.get("/{city_id}")
async def read_city(city_id: int, service: ReadCity) -> ReadCityResponse:
    return await service.execute(city_id)


@router.get("/")
async def read_cities(service: ReadCities, schema: ReadCitiesRequest = Depends()) -> ReadCitiesResponse:
    return ReadCitiesResponse(cities=[city async for city in service.execute(schema)])


@router.patch("/{city_id}")
async def update_city(city_id: int, service: UpdateCity, schema: UpdateCityRequest) -> UpdateCityResponse:
    return await service.execute(city_id, schema)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, service: DeleteCity) -> None:
    return await service.execute(city_id)

from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.cities.schemas import ReadCityResponse
from app.apps.cities.schemas import UpdateCityResponse
from app.base.exceptions import NotFoundError
from app.base.services import read_by_id
from app.models.cities import City
from tests.utils import clean_response
from tests.utils import create_instances
from tests.utils import to_json


async def test_cities_read_all(ac: AsyncClient, session: AsyncSession) -> None:
    instances_qty = 4
    cities = [city async for city in create_instances(session, City, instances_qty)]

    response = await ac.get("/cities/")

    assert status.HTTP_200_OK == response.status_code

    response_data = response.json()["cities"]

    for i, city in enumerate(cities):
        assert to_json(city, ReadCityResponse) == response_data[i]


async def test_cities_read_by_id(ac: AsyncClient, session: AsyncSession) -> None:
    city = [instance async for instance in create_instances(session, City)][0]
    response = await ac.get(f"/cities/{city.id}")

    assert status.HTTP_200_OK == response.status_code
    assert to_json(city, ReadCityResponse) == response.json()


async def test_cities_read_city_that_does_not_exists(ac: AsyncClient, session: AsyncSession) -> None:
    response = await ac.get("/cities/1")
    assert status.HTTP_404_NOT_FOUND == response.status_code
    assert "Not found" == response.json()["detail"]


async def test_cities_create(ac: AsyncClient, session: AsyncSession) -> None:
    request_data = {"name": "City-1", "longitude": 1.0, "latitude": 1.0}

    response = await ac.post("/cities/", json=request_data)

    assert status.HTTP_201_CREATED == response.status_code

    assert request_data == clean_response(response, "id", "created_at", "updated_at")


async def test_create_city_with_already_existing_name(ac: AsyncClient, session: AsyncSession) -> None:
    city = [instance async for instance in create_instances(session, City)][0]
    request_data = {"name": city.name, "longitude": 1.0, "latitude": 1.0}

    response = await ac.post("/cities/", json=request_data)

    assert status.HTTP_400_BAD_REQUEST == response.status_code

    expected = f"The city with name {city.name} already exists"
    assert expected == response.json()["detail"]


async def test_cities_update(ac: AsyncClient, session: AsyncSession) -> None:
    city = [instance async for instance in create_instances(session, City)][0]

    request_data = {
        "name": "Updated City",
        "longitude": 30,
        "latitude": 80,
    }

    response = await ac.put(f"/cities/{city.id}", json=request_data)

    assert status.HTTP_200_OK == response.status_code

    await session.refresh(city)
    assert to_json(city, UpdateCityResponse) == response.json()


async def test_update_city_that_does_not_exists(ac: AsyncClient, session: AsyncSession) -> None:
    request_data = {
        "name": "Updated City",
        "longitude": 30,
        "latitude": 80,
    }

    response = await ac.put("/cities/1", json=request_data)

    assert status.HTTP_404_NOT_FOUND == response.status_code
    assert "Not found" == response.json()["detail"]


async def test_update_city_name_to_already_existing(ac: AsyncClient, session: AsyncSession) -> None:
    city_0, city_1 = [instance async for instance in create_instances(session, City, 2)][:2]

    request_data = {
        "name": city_1.name,
        "longitude": 30,
        "latitude": 80,
    }

    response = await ac.put(f"/cities/{city_0.id}", json=request_data)

    assert status.HTTP_400_BAD_REQUEST == response.status_code

    expected = f"The city with name {city_1.name} already exists"
    assert expected == response.json()["detail"]


async def test_cities_delete(ac: AsyncClient, session: AsyncSession) -> None:
    city = [instance async for instance in create_instances(session, City)][0]

    response = await ac.delete(f"/cities/{city.id}")

    assert status.HTTP_204_NO_CONTENT == response.status_code

    try:
        await read_by_id(session, City, city.id)
        assert False
    except NotFoundError:
        assert True

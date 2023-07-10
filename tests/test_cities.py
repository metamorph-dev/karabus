import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.cities.models import City
from app.base.services import read_all
from app.base.services import read_by_id
from tests.utils import clean_response_data
from tests.utils import create_test_cities


@pytest.mark.asyncio
async def test_cities_read_all(ac: AsyncClient, session: AsyncSession) -> None:
    await create_test_cities(session, 4)

    response = await ac.get("/cities/")

    assert response.status_code == 200
    expected = [
        {
            "name": "City-4",
            "longitude": 4,
            "latitude": 4,
        },
        {
            "name": "City-3",
            "longitude": 3,
            "latitude": 3,
        },
        {
            "name": "City-2",
            "longitude": 2,
            "latitude": 2,
        },
        {
            "name": "City-1",
            "longitude": 1,
            "latitude": 1,
        },
    ]

    response_data = response.json()["cities"]
    assert expected == [clean_response_data(item) for item in response_data]


@pytest.mark.asyncio
async def test_cities_read_by_id(ac: AsyncClient, session: AsyncSession) -> None:
    await create_test_cities(session)

    city = [city async for city in read_all(session, City)][0]
    response = await ac.get(f"/cities/{city.id}")

    assert response.status_code == 200

    response_data = clean_response_data(response.json())
    assert response_data["name"] == city.name
    assert response_data["longitude"] == city.longitude
    assert response_data["latitude"] == city.latitude


@pytest.mark.asyncio
async def test_cities_create(ac: AsyncClient, session: AsyncSession) -> None:
    request_data = {"name": "City-1", "longitude": 1.0, "latitude": 1.0}

    response = await ac.post("/cities/", json=request_data)

    assert response.status_code == 201

    response_data = clean_response_data(response.json())
    assert request_data == response_data


@pytest.mark.asyncio
async def test_create_city_with_already_existing_name(ac: AsyncClient, session: AsyncSession) -> None:
    await create_test_cities(session)

    city = [city async for city in read_all(session, City)][0]

    request_data = {"name": city.name, "longitude": 1.0, "latitude": 1.0}

    response = await ac.post("/cities/", json=request_data)

    assert response.status_code == 400
    assert response.json()["detail"] == f"The city with name {request_data['name']} already exists"


@pytest.mark.asyncio
async def test_cities_update(ac: AsyncClient, session: AsyncSession) -> None:
    await create_test_cities(session)
    city = [city async for city in read_all(session, City)][0]
    assert city.name == "City-1"

    request_data = {
        "name": "Updated City",
        "longitude": 30,
        "latitude": 80,
    }

    response = await ac.put(f"/cities/{city.id}", json=request_data)

    assert response.status_code == 200

    response_data = clean_response_data(response.json())
    assert response_data == request_data

    await session.refresh(city)
    assert city.name == request_data["name"]
    assert city.longitude == request_data["longitude"]
    assert city.latitude == request_data["latitude"]


@pytest.mark.asyncio
async def test_update_city_name_to_already_existing(ac: AsyncClient, session: AsyncSession) -> None:
    await create_test_cities(session, 2)
    city2 = [city async for city in read_all(session, City)][0]
    city1 = [city async for city in read_all(session, City)][1]
    assert city1.name == "City-1"
    assert city2.name == "City-2"

    request_data = {
        "name": city1.name,
        "longitude": 30,
        "latitude": 80,
    }

    response = await ac.put(f"/cities/{city2.id}", json=request_data)

    assert response.status_code == 400
    assert response.json()["detail"] == f"The city with name {city1.name} already exists"


@pytest.mark.asyncio
async def test_notes_delete(ac: AsyncClient, session: AsyncSession) -> None:
    await create_test_cities(session)

    city = [city async for city in read_all(session, City)][0]

    response = await ac.delete(f"/cities/{city.id}")

    assert response.status_code == 204

    assert (await read_by_id(session, City, city.id)) is None

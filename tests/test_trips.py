from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.trips.schemas import CreateTripResponse
from app.apps.trips.schemas import ReadTripResponse
from app.models import Bus
from app.models import City
from app.models import Trip
from tests.utils import clean_response
from tests.utils import create_instances
from tests.utils import get_trip_by_id
from tests.utils import to_json


async def test_trips_read_all(ac: AsyncClient, session: AsyncSession) -> None:
    # Arrange
    trip = [trip async for trip in create_instances(session, Trip)][0]

    # Act
    response = await ac.get("/trips/")

    # Assert
    assert status.HTTP_200_OK == response.status_code

    response_data = response.json()["trips"][0]

    trip = await get_trip_by_id(session, trip.id)
    assert to_json(trip, ReadTripResponse) == response_data


async def test_trips_read_by_id(ac: AsyncClient, session: AsyncSession) -> None:
    trip = [trip async for trip in create_instances(session, Trip)][0]

    response = await ac.get(f"/trips/{trip.id}")

    assert 200 == response.status_code

    trip = await get_trip_by_id(session, trip.id)
    assert to_json(trip, ReadTripResponse) == response.json()


async def test_trips_create(ac: AsyncClient, session: AsyncSession) -> None:
    bus = [bus async for bus in create_instances(session, Bus)][0]
    city_1, city_2 = [city async for city in create_instances(session, City, 2)][:2]

    await session.refresh(bus)
    await session.refresh(city_1)
    await session.refresh(city_2)

    request_data = {
        "name": "Good Trip",
        "bus_id": bus.id,
        "price": 9999,
        "stops": [
            {
                "city_id": city_1.id,
                "datetime": "2023-07-14T06:48:58.305000+00:00",
            },
            {
                "city_id": city_2.id,
                "datetime": "2023-07-14T06:48:58.305000+00:00",
            },
        ]
    }

    response = await ac.post("/trips/", json=request_data)
    response_data = clean_response(response, "stops")

    assert status.HTTP_201_CREATED == response.status_code

    trip = await get_trip_by_id(session, response_data["id"])
    assert to_json(trip, CreateTripResponse, exclude={"stops"}) == response_data


async def test_trips_delete(ac: AsyncClient, session: AsyncSession) -> None:
    trip = [trip async for trip in create_instances(session, Trip)][0]

    response = await ac.delete(f"/trips/{trip.id}")
    assert status.HTTP_204_NO_CONTENT == response.status_code


async def test_trips_update(ac: AsyncClient, session: AsyncSession) -> None:
    trip = [trip async for trip in create_instances(session, Trip)][0]
    bus = [bus async for bus in create_instances(session, Bus)][0]

    await session.refresh(trip)
    await session.refresh(bus)

    request_data = {
        "name": "updated good trip",
        "price": 4000,
        "bus_id": bus.id,
        "seats_left": 2,
    }

    response = await ac.put(f"/trips/{trip.id}", json=request_data)
    response_data = response.json()

    assert status.HTTP_200_OK == response.status_code

    await session.refresh(trip)
    trip = await get_trip_by_id(session, trip.id)
    assert to_json(trip, ReadTripResponse) == response_data

from httpx import AsyncClient

from app.apps.busses.enums import Color
from app.apps.busses.models import Bus
from app.apps.busses.schemas import ReadBusResponse
from app.apps.busses.schemas import UpdateBusResponse
from app.base.exceptions import NotFoundError
from app.base.services import read_by_id
from app.db import AsyncSession
from tests.utils import clean_response
from tests.utils import create_instances
from tests.utils import to_json


async def test_busses_read_all(ac: AsyncClient, session: AsyncSession) -> None:
    instances_qty = 4
    busses = [bus async for bus in create_instances(session, Bus, instances_qty)]

    response = await ac.get("/busses/")

    assert 200 == response.status_code

    response_data = response.json()["busses"]
    for i, bus in enumerate(busses):
        assert to_json(bus, ReadBusResponse) == response_data[i]


async def test_busses_read_by_id(ac: AsyncClient, session: AsyncSession) -> None:
    bus = [instance async for instance in create_instances(session, Bus)][0]

    response = await ac.get(f"/busses/{bus.id}")

    assert 200 == response.status_code
    assert to_json(bus, ReadBusResponse) == response.json()


async def test_busses_create(ac: AsyncClient, session: AsyncSession) -> None:
    request_data = {"color": Color.BLUE, "seats_quantity": 8, "number_plate": "АХ1221HI"}

    response = await ac.post("/busses/", json=request_data)

    assert 201 == response.status_code
    assert request_data == clean_response(response, "id", "created_at", "updated_at")


async def test_create_bus_with_invalid_number_plate_4_digits_in_the_middle(
        ac: AsyncClient, session: AsyncSession
) -> None:
    request_data = {"color": Color.BLUE, "seats_quantity": 8, "number_plate": "АХi221HI"}
    response = await ac.post("/busses/", json=request_data)

    assert 422 == response.status_code

    expected = {
        "detail": [
            {
                "loc": ["body", "number_plate"],
                "msg": "Must be 4 digits in the middle",
                "type": "value_error",
            }
        ]
    }
    assert expected == response.json()


async def test_create_bus_with_invalid_number_plate_first_2_chars(
        ac: AsyncClient, session: AsyncSession
) -> None:
    request_data = {"color": Color.BLUE, "seats_quantity": 8, "number_plate": "А01221HI"}
    response = await ac.post("/busses/", json=request_data)

    assert 422 == response.status_code

    expected = {
        "detail": [
            {
                "loc": ["body", "number_plate"],
                "msg": "First 2 characters must be letters",
                "type": "value_error",
            }
        ]
    }
    assert expected == response.json()


async def test_create_bus_with_invalid_number_plate_last_2_chars(
        ac: AsyncClient, session: AsyncSession
) -> None:
    request_data = {"color": Color.BLUE, "seats_quantity": 8, "number_plate": "АH1221H1"}
    response = await ac.post("/busses/", json=request_data)

    assert 422 == response.status_code

    expected = {
        "detail": [
            {
                "loc": ["body", "number_plate"],
                "msg": "Last 2 characters must be letters",
                "type": "value_error",
            }
        ]
    }
    assert expected == response.json()


async def test_create_bus_with_already_existing_number_plate(ac: AsyncClient, session: AsyncSession) -> None:
    bus = [instance async for instance in create_instances(session, Bus)][0]
    request_data = {"color": Color.BLUE, "seats_quantity": 8, "number_plate": bus.number_plate}

    response = await ac.post("/busses/", json=request_data)

    assert 400 == response.status_code

    expected = f"The bus with number plate {bus.number_plate} already exists"
    assert expected == response.json()["detail"]


async def test_busses_update(ac: AsyncClient, session: AsyncSession) -> None:
    bus = [instance async for instance in create_instances(session, Bus)][0]

    request_data = {
        "color": Color.RED,
        "seats_quantity": 6,
        "number_plate": "АХ1221HI",
    }

    response = await ac.put(f"/busses/{bus.id}", json=request_data)

    assert 200 == response.status_code

    await session.refresh(bus)
    assert to_json(bus, UpdateBusResponse) == response.json()


async def test_update_city_number_plate_to_already_existing(ac: AsyncClient, session: AsyncSession) -> None:
    bus_0, bus_1 = [instance async for instance in create_instances(session, Bus, 2)][:2]

    request_data = {
        "color": Color.RED,
        "seats_quantity": 6,
        "number_plate": bus_1.number_plate,
    }

    response = await ac.put(f"/busses/{bus_0.id}", json=request_data)
    assert 400 == response.status_code

    expected = f"The bus with number plate {bus_1.number_plate} already exists"
    assert expected == response.json()["detail"]


async def test_busses_delete(ac: AsyncClient, session: AsyncSession) -> None:
    bus = [instance async for instance in create_instances(session, Bus)][0]

    response = await ac.delete(f"/busses/{bus.id}")
    assert 204 == response.status_code

    try:
        await read_by_id(session, Bus, bus.id)
        assert False
    except NotFoundError:
        assert True

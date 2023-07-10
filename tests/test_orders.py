from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.orders.schemas import CreateOrderResponse
from app.apps.orders.schemas import OrderSchema
from app.apps.orders.schemas import ReadOrderResponse
from app.apps.orders.services.read_order_by_id import read_order_by_id
from app.models import Order
from app.models import Trip
from tests.utils import create_instances
from tests.utils import to_json


async def test_orders_read_all(ac: AsyncClient, session: AsyncSession) -> None:
    orders = [order async for order in create_instances(session, Order, 4)][:4]

    response = await ac.get("/orders/")
    assert status.HTTP_200_OK == response.status_code

    response_data = response.json()["orders"]

    for response_data_item, order in zip(response_data, orders):
        assert to_json(order, OrderSchema) == response_data_item


async def test_orders_read_by_id(ac: AsyncClient, session: AsyncSession) -> None:
    order = [order async for order in create_instances(session, Order)][0]

    response = await ac.get(f"/orders/{order.id}")
    assert 200 == response.status_code

    order = await read_order_by_id(session, order.id)
    assert to_json(order, ReadOrderResponse) == response.json()


async def test_orders_create(ac: AsyncClient, session: AsyncSession) -> None:
    trip = [trip async for trip in create_instances(session, Trip)][0]

    await session.refresh(trip)

    request_data = {
        "trip_id": trip.id,
        "price": 1000_00,
        "passengers": [
            {
                "first_name": "Alex",
                "last_name": "Johnson",
                "ticket_price": 1000_00,
                "age": 27,
            },
        ]
    }

    response = await ac.post("/orders/", json=request_data)
    response_data = response.json()

    assert status.HTTP_201_CREATED == response.status_code

    order = await read_order_by_id(session, response_data["id"])
    assert to_json(order, CreateOrderResponse) == response_data

from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.users.schemas import LoginSchema
from app.apps.users.services.create_user import create_user
from app.base.services import read_by_id
from app.models import Order
from app.models import Trip
from tests.utils import create_instances


async def test_create_user(ac: AsyncClient, session: AsyncSession) -> None:
    request_data = {
        "username": "test_user",
        "password": "qwe123",
    }

    response = await ac.post("/users/", json=request_data)
    assert status.HTTP_201_CREATED == response.status_code

    response_data = response.json()
    expected = {
        "username": request_data["username"],
        "active": "True",
    }
    assert expected == response_data


async def test_create_user_when_user_already_exists(ac: AsyncClient, session: AsyncSession) -> None:
    request_data = {
        "username": "test_user",
        "password": "qwe123",
    }

    response = await ac.post("/users/", json=request_data)
    assert status.HTTP_201_CREATED == response.status_code

    response = await ac.post("/users/", json=request_data)
    assert status.HTTP_400_BAD_REQUEST == response.status_code
    assert f"User with username {request_data['username']} already exists" == response.json()["detail"]


async def test_login(ac: AsyncClient, session: AsyncSession) -> None:
    creds = {
        "username": "test_user",
        "password": "qwe123",
    }
    await create_user(session, LoginSchema(**creds))

    response = await ac.post("/users/token", json=creds)
    assert status.HTTP_200_OK == response.status_code
    assert response.json().get("access_token") is not None


async def test_login_with_wrong_password(ac: AsyncClient, session: AsyncSession) -> None:
    creds = {
        "username": "test_user",
        "password": "qwe123",
    }
    await create_user(session, LoginSchema(**creds))

    response = await ac.post("/users/token", json=creds | {"password": "wrong"})
    assert status.HTTP_401_UNAUTHORIZED == response.status_code

    expected = {"detail": "Incorrect username or password"}
    assert expected == response.json()


async def test_my_orders(ac: AsyncClient, session: AsyncSession) -> None:
    trip = [trip async for trip in create_instances(session, Trip)][0]
    creds = {
        "username": "test_user",
        "password": "qwe123",
    }
    user = await create_user(session, LoginSchema(**creds))
    response = await ac.post("/users/token", json=creds)
    token = response.json()["access_token"]

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
    headers = {"Authorization": f"Bearer {token}"}

    response = await ac.post("/orders/", json=request_data, headers=headers)
    assert status.HTTP_201_CREATED == response.status_code

    order_id = response.json()["id"]
    order = await read_by_id(session, Order, order_id)
    assert user.id == order.user_id

    response = await ac.get("/orders/my", headers=headers)
    assert status.HTTP_200_OK == response.status_code


async def test_read_my_orders_as_anonymous_user(ac: AsyncClient, session: AsyncSession) -> None:
    response = await ac.get("/orders/my")
    assert status.HTTP_403_FORBIDDEN == response.status_code
    assert "Forbidden" == response.json()["detail"]

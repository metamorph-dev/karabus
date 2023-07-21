import json
import random
import string
from datetime import datetime
from datetime import timedelta
from functools import partial
from typing import AsyncIterator
from typing import Callable
from typing import Sequence
from typing import Type
from typing import TypeVar

from httpx import Response
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload

from app.apps.busses.enums import Color
# from app.apps.orders.enums import OrderStatus
# from app.apps.orders.services.read_orders import read_orders
# from app.base.services import read_all
from app.models import Base
from app.models import Bus
from app.models import City
# from app.models import Order
# from app.models import Passenger
# from app.models import Trip
# from app.models import TripStop


T = TypeVar("T", bound=Base)

get_random = partial(random.randint, a=1, b=10_000_000)


# def _create_passenger(i: int) -> Passenger:
#     return Passenger(
#         first_name=f"Passenger {i}",
#         last_name=f"Passenger {i}",
#         ticket_price=random.randint(1, 1_000),
#         age=random.randint(20, 40)
#     )


# def _create_order(i: int) -> Order:
#     return Order(
#         trip=_create_trip(i),
#         price=random.randint(1, 1_000),
#         status=OrderStatus.PENDING,
#         passengers=[_create_passenger(get_random()) for _ in range(random.randint(1, 6))]
#     )


# def _create_trip_stop(i: int) -> TripStop:
#     return TripStop(
#         city=_create_city(i),
#         datetime=datetime.utcnow() + timedelta(days=random.randint(1, 14))
#     )
#
#
# def _create_trip(i: int) -> Trip:
#     bus = _create_bus(get_random())
#
#     return Trip(
#         name=f"Trip-{i}",
#         price=i * 100,
#         seats_left=bus.seats_quantity,
#         bus=bus,
#         stops=[
#             _create_trip_stop(get_random()),
#             _create_trip_stop(get_random()),
#         ],
#     )
#
#
# async def get_trip_by_id(session: AsyncSession, trip_id: int) -> Trip:
#     query = (
#         select(Trip)
#         .options(
#             joinedload(Trip.bus),
#             selectinload(Trip.stops),
#         )
#         .where(Trip.id == trip_id)
#     )
#     return await session.scalar(query)


def _create_city(i: int) -> City:
    return City(name=f"City-{i}", longitude=i, latitude=i)


def _generate_bus_number_plate(index: int) -> str:
    result = ""
    for i in range(8):
        ch_index = index % 10
        index //= 10

        if i in (0, 1, 6, 7):
            ch_index = string.ascii_uppercase[ch_index]

        result += str(ch_index)

    return result[::-1]


def _create_bus(i: int) -> Bus:
    return Bus(
        color=random.choice(list(Color)),
        seats_quantity=50,
        number_plate=_generate_bus_number_plate(i),
    )


fabrics: dict[Type[T], Callable[[int], T]] = {
    City: _create_city,
    Bus: _create_bus,
    # Trip: _create_trip,
    # Order: _create_order,
}

read_items_functions: dict[Type[T], Callable[[AsyncSession, int | None, int | None], AsyncIterator[T]]] = {
    # Order: read_orders
}


async def create_instances(session: AsyncSession, model: Type[T], qty: int = 1) -> AsyncIterator[T]:
    create_instance = fabrics[model]
    read_items = read_items_functions.get(model, partial(read_all, model=model))

    session.add_all((create_instance(get_random()) for _ in range(1, qty + 1)))
    await session.flush()
    await session.commit()

    async for item in read_items(session):
        yield item


def to_json(instance: T, schema: Type[BaseModel], *args, **kwargs) -> dict:
    return json.loads(schema.from_orm(instance).json(*args, **kwargs))


def clean_response(response: Response, *excluded_fields: Sequence[str]) -> dict:
    return {key: value for key, value in response.json().items() if key not in excluded_fields}

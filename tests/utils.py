import json
import random
import string
from typing import AsyncIterator
from typing import Callable
from typing import Sequence
from typing import Type
from typing import TypeVar

from httpx import Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.busses.enums import Color
from app.apps.busses.models import Bus
from app.apps.cities.models import City
from app.base.models import Base
from app.base.services import read_all


T = TypeVar("T", bound=Base)


def create_city(i: int) -> City:
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
        seats_quantity=random.randint(1, 10),
        number_plate=_generate_bus_number_plate(i),
    )


fabrics: dict[Type[T], Callable[[int], T]] = {
    City: create_city,
    Bus: _create_bus,
}


async def create_instances(session: AsyncSession, model: Type[T], qty: int = 1) -> AsyncIterator[T]:
    create_instance = fabrics[model]

    session.add_all((create_instance(i) for i in range(1, qty + 1)))
    await session.flush()
    await session.commit()
    async for item in read_all(session, model):
        yield item


def to_json(instance: T, schema: Type[BaseModel], *args, **kwargs) -> dict:
    return json.loads(schema.from_orm(instance).json(*args, **kwargs))


def clean_response(response: Response, *excluded_fields: Sequence[str]) -> dict:
    return {key: value for key, value in response.json().items() if key not in excluded_fields}

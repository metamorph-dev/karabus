from typing import AsyncIterator

from app.apps.orders.enums import OrderStatus
from app.apps.orders.schemas import CreateOrderRequest
from app.apps.orders.schemas import CreateOrderResponse
from app.apps.orders.schemas import OrderSchema
from app.apps.orders.schemas import ReadOrderResponse
from app.apps.orders.services.create_order import create_order
from app.apps.orders.services.read_order_by_id import read_order_by_id
from app.apps.orders.services.read_orders import read_orders
from app.apps.orders.services.update_order_status import update_order_status
from app.db import AsyncSession


class CreateOrder:
    def __init__(self, session: AsyncSession):
        self.async_session = session

    async def execute(self, data: CreateOrderRequest) -> CreateOrderResponse:
        async with self.async_session.begin() as session:
            session: AsyncSession

            order = await create_order(session, data)
            order = await read_order_by_id(session, order.id)

            return CreateOrderResponse.from_orm(order)


class ReadOrder:
    def __init__(self, session: AsyncSession):
        self.async_session = session

    async def execute(self, order_id: int) -> ReadOrderResponse:
        async with self.async_session.begin() as session:
            session: AsyncSession

            order = await read_order_by_id(session, order_id)
            return ReadOrderResponse.from_orm(order)


class ReadAllOrder:
    def __init__(self, session: AsyncSession):
        self.async_session = session

    async def execute(self, offset: int = 0, limit: int = 50) -> AsyncIterator[OrderSchema]:
        async with self.async_session.begin() as session:
            session: AsyncSession

            async for order in read_orders(session, offset, limit):
                yield OrderSchema.from_orm(order)


class ConfirmPayment:
    def __init__(self, session: AsyncSession):
        self.async_session = session

    async def execute(self, order_id: int, status: OrderStatus) -> None:
        async with self.async_session.begin() as session:
            session: AsyncSession

            order = await read_order_by_id(session, order_id)
            await update_order_status(session, order, status)

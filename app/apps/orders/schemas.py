from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

from app.apps.orders.enums import OrderStatus


class PassengerSchema(BaseModel):
    id: int
    created: datetime
    updated: datetime

    first_name: str
    last_name: str
    ticket_price: int
    age: int

    class Config:
        orm_mode = True


class OrderSchema(BaseModel):
    id: int
    created: datetime
    updated: datetime

    status: OrderStatus
    price: int
    trip_id: int
    passengers: list[PassengerSchema]

    class Config:
        orm_mode = True


class CreatePassengerRequest(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    ticket_price: int = Field(gt=0)
    age: int = Field(gt=0)


class CreatePassengerResponse(PassengerSchema):
    ...


class CreateOrderRequest(BaseModel):
    trip_id: int
    passengers: list[CreatePassengerRequest] = Field(min_items=1)
    price: int = Field(gt=0)


class CreateOrderResponse(OrderSchema):
    ...


class UpdateOrderRequest(BaseModel):
    trip_id: int
    price: int


class UpdateOrderResponse(OrderSchema):
    ...


class ReadAllOrderResponse(BaseModel):
    orders: list[OrderSchema]


class ReadOrderResponse(OrderSchema):
    ...

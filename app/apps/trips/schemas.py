from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

from app.apps.busses.schemas import BusSchema


class TripStopSchema(BaseModel):
    trip_id: int
    city_id: int
    datetime: datetime

    class Config:
        orm_mode = True


class CreateTripStopRequest(BaseModel):
    city_id: int
    datetime: datetime


class TripSchema(BaseModel):
    id: int
    name: str
    price: int
    seats_left: int
    bus: BusSchema
    stops: list[TripStopSchema]

    class Config:
        orm_mode = True


class CreateTripRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=64)
    price: int = Field(ge=0)
    bus_id: int
    stops: list[CreateTripStopRequest] = Field(min_items=2)


class CreateTripResponse(TripSchema):
    ...


class ReadTripResponse(TripSchema):
    ...


class ReadAllTripResponse(BaseModel):
    trips: list[TripSchema]


class UpdateTripRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=64)
    price: int = Field(ge=0)
    bus_id: int
    seats_left: int = Field(ge=0)


class UpdateTripResponse(TripSchema):
    ...

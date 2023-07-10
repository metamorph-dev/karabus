from datetime import datetime

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from app.apps.busses.enums import Color
from app.apps.busses.validators import validate_number_plate


class BusSchema(BaseModel):
    id: int
    color: Color
    seats_quantity: int
    number_plate: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CreateBusRequest(BaseModel):
    color: Color
    seats_quantity: int = Field(ge=0)
    number_plate: str = Field(min_length=8, max_length=8)

    @validator("number_plate")
    def validate_number_plate(cls, value: str) -> str:
        return validate_number_plate(value)


class CreateBusResponse(BusSchema):
    ...


class ReadBusResponse(BusSchema):
    ...


class ReadAllBusResponse(BaseModel):
    busses: list[BusSchema]


class UpdateBusRequest(CreateBusRequest):
    ...


class UpdateBusResponse(BusSchema):
    ...

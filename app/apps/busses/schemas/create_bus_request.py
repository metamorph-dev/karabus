from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

from app.apps.busses.enums import Color
from app.apps.busses.schemas.validators import validate_number_plate


class CreateBusRequest(BaseModel):
    number_plate: str = Field(min_length=8, max_length=8)
    seats_quantity: int = Field(gt=0)
    color: Color

    @field_validator("number_plate")
    def validate_number_plate(cls, value: str) -> str:
        return validate_number_plate(value)

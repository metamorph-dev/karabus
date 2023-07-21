from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

from app.apps.busses.enums import Color
from app.apps.busses.schemas.validators import validate_number_plate


class UpdateBusRequest(BaseModel):
    number_plate: str | None = Field(min_length=8, max_length=8, default=None)
    seats_quantity: int | None = Field(gt=0, default=None)
    color: Color | None = None

    @field_validator("number_plate")
    def validate_number_plate(cls, value: str) -> str:
        return validate_number_plate(value)

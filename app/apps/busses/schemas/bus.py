from pydantic import BaseModel

from app.apps.busses.enums import Color


class BusSchema(BaseModel):
    id: int
    number_plate: str
    seats_quantity: int
    color: Color

    class Config:
        from_attributes = True

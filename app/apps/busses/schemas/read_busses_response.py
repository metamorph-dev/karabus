from pydantic import BaseModel

from app.apps.busses.schemas.read_bus_response import ReadBusResponse


class ReadBussesResponse(BaseModel):
    busses: list[ReadBusResponse]

from pydantic import BaseModel
from pydantic import Field


class CreateCityRequest(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)

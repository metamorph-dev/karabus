from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class CitySchema(BaseModel):
    id: int
    name: str
    longitude: float
    latitude: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CreateCityRequest(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)


class CreateCityResponse(CitySchema):
    ...


class ReadCityResponse(CitySchema):
    ...


class ReadAllCitiesResponse(BaseModel):
    cities: list[CitySchema]


class UpdateCityRequest(CreateCityRequest):
    ...


class UpdateCityResponse(CitySchema):
    ...

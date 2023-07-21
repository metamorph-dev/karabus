from pydantic import BaseModel
from pydantic import Field


class UpdateCityRequest(BaseModel):
    name: str | None = Field(min_length=1, max_length=64, default=None)
    longitude: float | None = Field(ge=-180, le=180, default=None)
    latitude: float | None = Field(ge=-90, le=90, default=None)

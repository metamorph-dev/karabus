from pydantic import BaseModel

from app.apps.cities.schemas.read_city_response import ReadCityResponse


class ReadCitiesResponse(BaseModel):
    cities: list[ReadCityResponse]

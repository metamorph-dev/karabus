from pydantic import BaseModel


class CitySchema(BaseModel):
    id: int
    name: str
    longitude: float
    latitude: float

    class Config:
        from_attributes = True

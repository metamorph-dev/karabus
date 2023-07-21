from pydantic import BaseModel
from pydantic import Field


class PaginationSchema(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(gt=0, default=50)

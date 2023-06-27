from datetime import datetime

from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.base.models import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column("id", autoincrement=True, unique=True, primary_key=True)
    name: Mapped[str] = mapped_column("name", String(64), unique=True)
    longitude: Mapped[float]
    latitude: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), server_onupdate=func.now())

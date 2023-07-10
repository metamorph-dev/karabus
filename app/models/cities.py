from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import Base


if TYPE_CHECKING:
    from app.models.trips import TripStop
    from app.models.trips import Trip


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column("id", autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column("name", String(64), unique=True)
    longitude: Mapped[float]
    latitude: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), server_onupdate=func.now())

    trips: Mapped[list["Trip"]] = relationship(secondary="trip_stops", back_populates="cities")
    stops: Mapped[list["TripStop"]] = relationship(
        back_populates="city", cascade="all, delete-orphan", overlaps="trips"
    )

from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import Base


if TYPE_CHECKING:
    from app.models.cities import City
    from app.models.trips import Trip


class TripStop(Base):
    __tablename__ = "trip_stops"

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"), primary_key=True)

    city: Mapped["City"] = relationship(back_populates="stops", overlaps="trips")
    trip: Mapped["Trip"] = relationship(back_populates="stops", overlaps="trips")

    datetime: Mapped[datetime]

    __mapper_args__ = {
        "confirm_deleted_rows": False,
    }

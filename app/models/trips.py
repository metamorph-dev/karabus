from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import Base


if TYPE_CHECKING:
    from app.models.busses import Bus
    from app.models.cities import City
    from app.models.trip_stop import TripStop


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    price: Mapped[int] = mapped_column(CheckConstraint("price >= 0"))
    seats_left: Mapped[int] = mapped_column(CheckConstraint("seats_left >= 0"))

    bus_id: Mapped[int] = mapped_column(ForeignKey("busses.id"))
    bus: Mapped["Bus"] = relationship(back_populates="trips")

    cities: Mapped[list["City"]] = relationship(
        secondary="trip_stops", back_populates="trips", overlaps="trip, city, stops"
    )
    stops: Mapped[list["TripStop"]] = relationship(
        back_populates="trip", order_by="TripStop.datetime", cascade="all, delete-orphan", overlaps="trips, cities"
    )

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint
from sqlalchemy import SmallInteger
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.apps.busses.enums import Color
from app.models.base import Base


if TYPE_CHECKING:
    from app.models.trips import Trip


class Bus(Base):
    __tablename__ = "busses"

    id: Mapped[int] = mapped_column("id", autoincrement=True, primary_key=True)
    color: Mapped[Color]
    seats_quantity: Mapped[int] = mapped_column("seats_quantity", SmallInteger, CheckConstraint("seats_quantity >= 0"))
    number_plate: Mapped[str] = mapped_column("number_plate", String(8), unique=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    trips: Mapped[list["Trip"]] = relationship(back_populates="bus")
    photo_filename: Mapped[str | None] = mapped_column(String(42))

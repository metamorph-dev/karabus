from datetime import datetime

from sqlalchemy import CheckConstraint
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.apps.busses.enums import Color
from app.db.base import Base


class Bus(Base):
    __tablename__ = "bus"
    __table_args__ = (
        CheckConstraint(text("seats_quantity >= 0")),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), server_onupdate=func.now())

    number_plate: Mapped[str] = mapped_column(String(8), unique=True)
    seats_quantity: Mapped[int]
    color: Mapped[Color]

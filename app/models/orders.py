from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.apps.orders.enums import OrderStatus
from app.models.base import Base


if TYPE_CHECKING:
    from app.models.trips import Trip
    from app.models.passengers import Passenger
    from app.models.users import User


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (CheckConstraint("price >= 0"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), server_onupdate=func.now())

    status: Mapped[OrderStatus]
    price: Mapped[int]

    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"))
    trip: Mapped["Trip"] = relationship(back_populates="orders")

    passengers: Mapped[list["Passenger"]] = relationship(back_populates="order", cascade="all, delete-orphan")

    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="orders")

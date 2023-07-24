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
    from app.models.orders import Order


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), server_onupdate=func.now())

    username: Mapped[str] = mapped_column(String(32), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(256))
    active: Mapped[bool]

    orders: Mapped[list["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")

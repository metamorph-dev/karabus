from app.exceptions.base import Base


class NotFoundException(Base):
    default_message = "Not found"

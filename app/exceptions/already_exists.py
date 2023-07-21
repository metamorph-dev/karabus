from app.exceptions.base import Base


class AlreadyExistsException(Base):
    default_message = "Already exists"

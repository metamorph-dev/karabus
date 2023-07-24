class APIException(Exception):
    default_message: str | None = None

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class AlreadyExistError(Exception):
    """AlreadyExistError"""


class NotFoundError(Exception):
    """NotFoundError"""

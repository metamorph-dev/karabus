MESSAGE_TYPE = str | None


class Base(Exception):
    default_message: MESSAGE_TYPE = None

    def __init__(self, message: MESSAGE_TYPE = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)

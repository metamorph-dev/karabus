class NotEnoughSeats(Exception):
    default_message = "Not enough seats"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)

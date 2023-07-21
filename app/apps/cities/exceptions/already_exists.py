from app.exceptions.already_exists import AlreadyExistsException


class CityAlreadyExistsException(AlreadyExistsException):
    message_pattern = "The city with name {name} already exists"

    def __init__(self, name: str) -> None:
        self.name = name
        self.message = self.message_pattern.format(name=self.name)
        super().__init__(self.message)

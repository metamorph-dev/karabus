from app.exceptions.already_exists import AlreadyExistsException


class BusAlreadyExistsException(AlreadyExistsException):
    message_pattern = "The bus with number plate {number_plate} already exists"

    def __init__(self, number_plate: str) -> None:
        self.number_plate = number_plate
        self.message = self.message_pattern.format(number_plate=number_plate)
        super().__init__(self.message)

from app.exceptions.not_found import NotFoundException


class CityNotFoundException(NotFoundException):
    message_pattern = "There is no city with id {instance_id}"

    def __init__(self, instance_id: int) -> None:
        self.instance_id = instance_id
        self.message = self.message_pattern.format(instance_id=self.instance_id)
        super().__init__(self.message)

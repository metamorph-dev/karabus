from enum import StrEnum


class OrderStatus(StrEnum):
    PENDING = "pending"
    PAYED = "payed"
    FAILED = "failed"

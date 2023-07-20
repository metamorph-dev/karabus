from fastapi import HTTPException
from fastapi import status

from app.base.exceptions import APIException


class WrongCredentialsException(APIException):
    default_message = "Wrong credentials"


class InactiveUserException(APIException):
    default_message = "Inactive user"


class CredentialException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

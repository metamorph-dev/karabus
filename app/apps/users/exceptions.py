from fastapi import HTTPException
from fastapi import status

from app.base.exceptions import APIError


class WrongCredentialsError(APIError):
    default_message = "Wrong credentials"


class InactiveUserError(APIError):
    default_message = "Inactive user"


class CredentialError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

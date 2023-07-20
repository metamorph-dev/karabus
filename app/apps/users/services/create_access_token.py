from datetime import datetime
from datetime import timedelta

from jose import jwt

from app.apps.users.schemas import PayloadData
from app.settings import settings


def create_access_token(data: PayloadData, expires: timedelta | None = None) -> str:
    to_encode = data.dict()

    if expires:
        expire = datetime.utcnow() + expires
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_HASHING_ALGORITHM)
    return encoded_jwt

from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.users.exceptions import CredentialException
from app.apps.users.schemas import Claims
from app.apps.users.schemas import PayloadData
from app.apps.users.services.get_user import get_user
from app.models import User
from app.settings import settings


async def get_current_user(session: AsyncSession, token: HTTPAuthorizationCredentials | None) -> User | None:
    if token is None:
        return None

    try:
        payload = PayloadData(
            **jwt.decode(token.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_HASHING_ALGORITHM])
        )
    except (JWTError, ValidationError) as exc:
        raise CredentialException from exc

    claims = Claims(username=payload.sub)

    user = await get_user(session, claims.username)
    if not user:
        raise CredentialException

    if not user.active:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Inactive user")

    return user

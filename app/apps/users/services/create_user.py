from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.users.schemas import LoginSchema
from app.apps.users.services.get_hashed_password import get_hashed_password
from app.apps.users.services.get_user import get_user
from app.models import User


async def create_user(session: AsyncSession, schema: LoginSchema) -> User:
    user = User(
        username=schema.username,
        hashed_password=get_hashed_password(schema.password),
        active=True,
    )
    session.add(user)

    try:
        await session.flush()
    except IntegrityError:
        raise HTTPException(400, f"User with username {schema.username} already exists")

    return user

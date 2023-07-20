from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.users.schemas import UserSchema
from app.apps.users.services.get_user import get_user
from app.apps.users.services.verify_password import verify_password


async def authenticate_user(session: AsyncSession, username: str, password: str) -> UserSchema | None:
    user = await get_user(session, username)
    if not verify_password(password, user.hashed_password):
        return None

    return user

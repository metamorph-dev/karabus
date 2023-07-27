from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import User


async def get_user(session: AsyncSession, username: str) -> User | None:
    query = select(User).options(joinedload(User.orders)).where(User.username == username)
    user = await session.scalar(query)
    return user

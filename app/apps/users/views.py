from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.apps.users.schemas import LoginSchema
from app.apps.users.schemas import PayloadData
from app.apps.users.schemas import Token
from app.apps.users.schemas import UserSchema
from app.apps.users.services.authenticate_user import authenticate_user
from app.apps.users.services.create_access_token import create_access_token
from app.apps.users.services.create_user import create_user
from app.db import AsyncSession
from app.settings import Settings
from app.settings import get_settings


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/token")
async def login(form: LoginSchema, async_session: AsyncSession, settings: Settings = Depends(get_settings)) -> Token:
    async with async_session.begin() as session:
        user = await authenticate_user(session, form.username, form.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_IN_MINUTES)
        access_token = create_access_token(PayloadData(sub=user.username), access_token_expires)
        return Token(access_token=access_token, token_type=settings.TOKEN_TYPE)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register(
        async_session: AsyncSession,
        form: LoginSchema,
) -> UserSchema:
    async with async_session.begin() as session:
        result = await create_user(session, form)
        return UserSchema.from_orm(result)

from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Claims(BaseModel):
    username: str | None = None


class UserSchema(BaseModel):
    username: str
    active: str | None = None

    class Config:
        orm_mode = True


class UserWithHashedPassword(UserSchema):
    hashed_password: str


class PayloadData(BaseModel):
    sub: str

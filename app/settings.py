from functools import lru_cache

from pydantic import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    DB_URL: PostgresDsn = "postgresql+psycopg://postgres:postgres@postgres:5432/postgres"
    TEST_DB_URL: PostgresDsn = "postgresql+psycopg://postgres:postgres@localhost:5432"
    JWT_SECRET_KEY: str = "5abac2061bf0941ac2c542172f5ce73dbb8c95756f33e21259013b49f18723ed"
    JWT_HASHING_ALGORITHM: str = "HS256"
    JWT_EXPIRE_IN_MINUTES: int = 30

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

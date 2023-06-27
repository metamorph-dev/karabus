from functools import lru_cache

from pydantic import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    DB_URL: PostgresDsn = "postgresql+psycopg://postgres:postgres@postgres:5432/postgres"
    TEST_DB_URL: PostgresDsn = "postgresql+psycopg://postgres:postgres@localhost:5432"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

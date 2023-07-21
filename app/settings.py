from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+psycopg://postgres:postgres@postgres:5432/postgres"
    TEST_DB_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

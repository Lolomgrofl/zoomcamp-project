from functools import lru_cache

from pydantic import MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    MYSQL_URL: MySQLDsn

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ZoomCamp API"


@lru_cache
def get_settings():
    return Settings()  # type: ignore


settings = get_settings()

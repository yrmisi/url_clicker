from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .path import BASE_DIR


class RedisTestConfig(BaseSettings):
    """Redis service configuration for tests."""

    password: Annotated[str | None, Field(alias="REDIS_PASSWORD")] = None
    host: Annotated[str, Field(alias="REDIS_HOST")] = "localhost"
    port: Annotated[int, Field(alias="REDIS_PORT")] = 6378
    db: int = 0
    short_url_limit: int = 3
    short_url_window: int = 5

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env.test",
        env_file_encoding="utf-8",
        extra="ignore",
    )

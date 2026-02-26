from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

from .path import BASE_DIR


class DataBaseConfig(BaseSettings):
    """Database service configuration."""

    user: Annotated[str | None, Field(alias="POSTGRES_USER")] = None
    password: Annotated[str | None, Field(alias="POSTGRES_PASSWORD")] = None
    host: Annotated[str, Field(alias="POSTGRES_HOST")] = "db"
    port: Annotated[int, Field(ge=1024, le=65535, alias="POSTGRES_PORT")] = 5432
    name: Annotated[str | None, Field(alias="POSTGRES_DB")] = None
    driver: str = "asyncpg"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / "envs" / ".env.postgres-prod",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def sqal_pg_url(self) -> URL:
        """Create a URL to connect to the database."""
        return URL.create(
            drivername=f"postgresql+{self.driver}",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )

from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

from .paths import ENVS_DIR


class DataBaseConfig(BaseSettings):
    """Database service configuration."""

    user: Annotated[str | None, Field(alias="POSTGRES_USER")] = None
    password: Annotated[str | None, Field(alias="POSTGRES_PASSWORD")] = None
    host: Annotated[str, Field(alias="POSTGRES_HOST")] = "db"
    port: Annotated[int, Field(ge=1024, le=65535, alias="POSTGRES_PORT")] = 5432
    name: Annotated[str | None, Field(alias="POSTGRES_DB")] = None
    driver: str = "asyncpg"
    pool_size: Annotated[int, Field(alias="POSTGRES_POOL_SIZE")] = 5
    max_overflow: Annotated[int, Field(alias="POSTGRES_MAX_OVERFLOW")] = 5
    pool_pre_ping: Annotated[bool, Field(alias="POSTGRES_POOL_PRE_PING")] = True
    pool_recycle: Annotated[int, Field(alias="POSTGRES_POOL_RECYCLE")] = 0
    pool_timeout: Annotated[int, Field(alias="POSTGRES_POOL_TIMEOUT")] = 10
    echo: Annotated[bool, Field(alias="POSTGRES_ECHO")] = True
    command_timeout: Annotated[int, Field(alias="POSTGRES_COMMAND_TIMEOUT")] = 30
    prepared_statement_cache_size: Annotated[
        int,
        Field(
            alias="POSTGRES_PREPARED_STATEMENT_CACHE_SIZE",
        ),
    ] = 0
    statement_cache_size: Annotated[int, Field(alias="POSTGRES_STATEMENT_CACHE_SIZE")] = 0
    isolation_level: Annotated[str, Field(alias="POSTGRES_ISOLATION_LEVEL")] = "AUTOCOMMIT"
    compiled_cache: Annotated[dict | None, Field(alias="POSTGRES_COMPILED_CACHE")] = None

    model_config = SettingsConfigDict(
        env_file=ENVS_DIR / ".env.postgres-prod",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def url_sqal_pg_async(self) -> URL:
        """Create a URL to connect to the database."""
        return URL.create(
            drivername=f"postgresql+{self.driver}",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )

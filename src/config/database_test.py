from pydantic_settings import SettingsConfigDict

from .database import DataBaseConfig
from .path import BASE_DIR


class DataBaseTestConfig(DataBaseConfig):
    """Database service configuration for tests."""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / "envs" / ".env.postgres-test",
        env_file_encoding="utf-8",
    )

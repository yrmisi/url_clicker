from pydantic_settings import SettingsConfigDict

from .database import DataBaseConfig
from .paths import ENVS_DIR


class DataBaseTestConfig(DataBaseConfig):
    """Database service configuration for tests."""

    model_config = SettingsConfigDict(
        env_file=ENVS_DIR / ".env.postgres-test",
        env_file_encoding="utf-8",
    )

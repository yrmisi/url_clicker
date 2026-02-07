from pydantic import BaseModel

from .database import DataBaseConfig
from .database_test import DataBaseTestConfig
from .redis import RedisConfig
from .redis_test import RedisTestConfig


class Settings(BaseModel):
    """Application service settings."""

    db: DataBaseConfig = DataBaseConfig()
    dbtest: DataBaseTestConfig = DataBaseTestConfig()
    redis_db: RedisConfig = RedisConfig()
    redis_test: RedisTestConfig = RedisTestConfig()


settings = Settings()

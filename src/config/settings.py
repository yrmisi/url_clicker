from pydantic import BaseModel

from .alembic import AlembicMigrationConfig
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
    abm: AlembicMigrationConfig = AlembicMigrationConfig()


settings = Settings()

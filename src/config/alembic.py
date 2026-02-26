from pydantic import BaseModel


class AlembicMigrationConfig(BaseModel):
    """Alembic migrate service configuration."""

    host: str = "db"
    port: int = 5432

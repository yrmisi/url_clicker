from pydantic import BaseModel


class AlembicMigrationConfig(BaseModel):
    """Alembic migrate service configuration."""

    driver: str = "psycopg2"
    host: str = "db"
    port: int = 5432
    # local migrate
    # host: str = "localhost"
    # port: int = 5435

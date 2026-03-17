from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings

engine = create_async_engine(
    settings.db.url_sqal_pg_async,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    pool_pre_ping=settings.db.pool_pre_ping,
    pool_recycle=settings.db.pool_recycle,
    pool_timeout=settings.db.pool_timeout,
    echo=settings.db.echo,
    connect_args=settings.db.get_connect_args,
    # execution_options для PgBouncer
    execution_options=settings.db.get_execution_options,
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

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
    connect_args={
        "command_timeout": settings.db.command_timeout,
        "prepared_statement_cache_size": settings.db.prepared_statement_cache_size,
        "statement_cache_size": settings.db.statement_cache_size,
    },
    # execution_options для PgBouncer
    execution_options={
        "isolation_level": settings.db.isolation_level,
        "compiled_cache": settings.db.compiled_cache,
    },
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

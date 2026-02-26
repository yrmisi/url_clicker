from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings

engine = create_async_engine(
    settings.db.url_sqal_pg_async,
    pool_size=10,  # базовое количество открытых соединений
    max_overflow=0,  # 0 для безопасности (не превышать лимит пула), 5 - макс. доп. соединений сверх pool_size
    pool_pre_ping=True,  # проверяет соединение перед использованием (избегает "broken pipe")
    pool_recycle=300,  # пересоздавать соединение каждые 5 минут (в секундах)
    pool_timeout=10,  # макс. время ожидания свободного соединения из пула
    # echo=False,  # отключить лог SQL (важно в production)
    connect_args={
        "command_timeout": 15,  # таймаут выполнения запроса (в секундах)
        "prepared_statement_cache_size": (
            0
        ),  # отключить для PgBouncer, 100 - кэш prepared statements (только для asyncpg)
        "statement_cache_size": 0,  # отключить для PgBouncer, 100 - кэш запросов
        # "server_settings": {"jit": "off"},  # отключить JIT (часто замедляет OLTP)
    },
    # execution_options для PgBouncer
    execution_options={
        "isolation_level": "AUTOCOMMIT",  # Для transaction pool_mode!
        "compiled_cache": None,  # Очистка кэша
    },
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

from functools import lru_cache

from redis.asyncio import Redis

from config import settings


@lru_cache
def get_redis() -> Redis:
    """ """
    return Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
        password=settings.redis.password,
    )

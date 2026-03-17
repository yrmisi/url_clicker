import random
from time import time

from redis.asyncio import Redis

from config import settings

from .redis_script import RATE_LIMIT_SCRIPT


class RateLimiter:
    def __init__(self, redis: Redis) -> None:
        """Initialize a rate limiter with the given Redis client."""
        self._redis = redis
        self._script = self._redis.register_script(RATE_LIMIT_SCRIPT)

    async def is_limited(
        self,
        ip_address: str,
        endpoint: str,
        max_requests: int,
        window_seconds: int,
    ) -> bool:
        """Return True if the IP has exceeded the max requests for the endpoint within the time window."""

        key: str = settings.redis.rate_limit_prefix.format(
            endpoint=endpoint,
            ip_address=ip_address,
        )
        now_ms: int = int(time() * 1000)
        window_start_ms: int = now_ms - (window_seconds * 1000)
        member: str = f"{now_ms}-{random.randint(0, 100_000)}"

        result: int = int(
            await self._script(
                keys=[key],
                args=[
                    now_ms,
                    window_start_ms,
                    max_requests,
                    member,
                    window_seconds,
                ],
            )
        )
        return bool(result)

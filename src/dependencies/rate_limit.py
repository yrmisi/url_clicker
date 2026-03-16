from typing import Annotated

from fastapi import Depends, Request
from fastapi.datastructures import Address
from redis.asyncio import Redis

from config import settings
from core import get_redis
from exceptions import RateLimitExceededError
from services import RateLimiter


def get_rate_limiter(r: Annotated[Redis, Depends(get_redis)]) -> RateLimiter:
    """Create a RateLimiter instance using the injected Redis client."""
    return RateLimiter(r)


def rate_limiter_factory(
    max_requests: int,
    window_seconds: int,
):
    """Return a dependency that enforces rate limiting with the given window and limit."""

    async def dependency(
        request: Request,
        rate_limiter: Annotated[RateLimiter, Depends(get_rate_limiter)],
    ) -> None:
        """Raise RateLimitExceededError if the client exceeds the allowed request rate."""

        client: Address | None = request.client
        if client is None:
            return

        ip_address: str = request.headers.get("x-forwarded-for", client.host).split(",")[0].strip()
        endpoint: str = request.url.path.strip("/").split("/")[-1]

        exceeded: bool = await rate_limiter.is_limited(
            ip_address,
            endpoint,
            max_requests,
            window_seconds,
        )
        if exceeded:
            raise RateLimitExceededError(
                window_seconds,
                max_requests,
            )

    return dependency


rate_limit_url = rate_limiter_factory(
    settings.redis.url_limit,
    settings.redis.url_window,
)

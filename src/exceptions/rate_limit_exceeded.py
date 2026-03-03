from fastapi import status

from .shortener_base import ShortenerBaseError


class RateLimitExceededError(ShortenerBaseError):
    """Request limit exceeded."""

    status_code: int = status.HTTP_429_TOO_MANY_REQUESTS
    detail: str = "Too many requests"

    def __init__(self, window_seconds: int, max_requests: int):
        self.window_seconds = window_seconds
        self.max_requests = max_requests
        self.detail = (
            f"You have exceeded your request limit. "
            f"Please try again in {window_seconds} seconds."
        )
        self.headers = {
            "Retry-After": str(window_seconds),
            "X-RateLimit-Limit": str(max_requests),
            "X-RateLimit-Remaining": "0",
        }
        super().__init__(self.detail)

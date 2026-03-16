from fastapi import status

from .shortener_base import ShortenerBaseError


class InvalidURLError(ShortenerBaseError):
    """Raised when the provided URL fails validation."""

    status_code: int = status.HTTP_422_UNPROCESSABLE_CONTENT
    detail: str = "invalid URL"

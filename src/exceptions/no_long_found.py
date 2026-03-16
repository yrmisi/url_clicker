from fastapi import status

from .shortener_base import ShortenerBaseError


class NoLongFoundError(ShortenerBaseError):
    """Raised when a long URL for the given slug cannot be found."""

    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "The link does not exist"

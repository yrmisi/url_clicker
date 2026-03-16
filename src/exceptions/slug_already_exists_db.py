from fastapi import status

from .shortener_base import ShortenerBaseError


class SlugAlreadyExistsDBError(ShortenerBaseError):
    """Raised when a unique slug cannot be generated after multiple attempts due to existing records in the database."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Failed to generate unique slug after 5 attempts"

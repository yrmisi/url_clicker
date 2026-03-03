from fastapi import status

from .shortener_base import ShortenerBaseError


class SlugAlreadyExistsDBError(ShortenerBaseError):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Failed to generate unique slug after 5 attempts"

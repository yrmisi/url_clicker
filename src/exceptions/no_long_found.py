from fastapi import status

from .shortener_base import ShortenerBaseError


class NoLongFoundError(ShortenerBaseError):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "The link does not exist"

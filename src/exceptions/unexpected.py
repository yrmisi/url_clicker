from fastapi import status

from .shortener_base import ShortenerBaseError


class UnexpectedError(ShortenerBaseError):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Unexpected error after 5 attempts"

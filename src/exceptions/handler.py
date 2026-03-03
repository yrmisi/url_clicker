from fastapi import Request, status
from fastapi.responses import JSONResponse

from .shortener_base import ShortenerBaseError


async def shortener_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global custom exception handler."""
    if isinstance(exc, ShortenerBaseError):
        headers: dict[str, str] | None = getattr(exc, "headers", None)
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=headers,
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

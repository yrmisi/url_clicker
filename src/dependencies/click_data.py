import re
from typing import Annotated

from fastapi import Depends, Request

from src.schemas import ClickData


def get_client_ip(request: Request) -> str | None:
    """Obtaining an IP via Nginx."""
    forwarded: str | None = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()

    real_ip: str | None = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip

    client = request.client
    if client:
        return client.host

    return None


def is_bot_request(user_agent: str | None) -> bool:
    """Simple bot detection."""
    if not user_agent:
        return True

    bot_patterns: list[str] = [
        r"bot|crawler|spider|scrapy",
        r"googlebot|yahoo|bingbot",
        r"facebookexternalhit|twitterbot",
        r"whatsapp|telegrambot",
    ]

    return any(re.findall(pattern, user_agent, re.IGNORECASE) for pattern in bot_patterns)


async def get_click_data(request: Request) -> ClickData:
    """Extracting all data for AnonymousClick."""
    return ClickData(
        session_id=request.cookies.get("session_id"),
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("user-agent"),
        accept_language=request.headers.get("accept-language"),
        referrer=request.headers.get("referer"),
        is_bot_suspected=is_bot_request(request.headers.get("user-agent")),
    )


ClickDataDep = Annotated[ClickData, Depends(get_click_data)]

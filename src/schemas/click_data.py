from dataclasses import dataclass


@dataclass
class ClickData:
    """Data extracted from request for AnonymousClick."""

    session_id: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    accept_language: str | None = None
    referrer: str | None = None
    is_bot_suspected: bool = False

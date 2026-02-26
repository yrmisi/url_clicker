from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .short_url import ShortURL


class AnonymousClick(Base):
    """Anonymous click on a short URL."""

    __tablename__ = "anonymous_clicks"

    short_url_id: Mapped[int] = mapped_column(
        ForeignKey("short_urls.id"),
        index=True,
    )
    session_id: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        index=True,
    )
    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
        index=True,
    )
    user_agent: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )
    accept_language: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )
    referrer: Mapped[str | None] = mapped_column(
        String(1048),
        nullable=True,
    )
    is_bot_suspected: Mapped[bool] = mapped_column(default=False)

    short_url: Mapped["ShortURL"] = relationship(
        back_populates="anonymous_clicks",
    )

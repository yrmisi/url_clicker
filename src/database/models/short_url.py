from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .anon_click import AnonymousClick


class ShortURL(Base):
    """ """

    __tablename__ = "short_urls"

    slug: Mapped[str] = mapped_column(
        String(length=6),
        unique=True,
    )
    long_url: Mapped[str] = mapped_column(String(length=2048))
    creation_count: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
    click_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    last_accessed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    anonymous_clicks: Mapped[list["AnonymousClick"]] = relationship(
        back_populates="short_url",
        cascade="all, delete",
    )

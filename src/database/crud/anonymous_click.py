from dataclasses import asdict

from src.dependencies import ClickDataDep

from ..dependencies import AsyncSessionDep
from ..models import AnonymousClick


async def add_anonymous_click_db(
    short_url_id: int,
    click_data: ClickDataDep,
    session: AsyncSessionDep,
) -> None:
    """Add anonymous click to database."""
    anonymous_click: AnonymousClick = AnonymousClick(
        short_url_id=short_url_id,
        **asdict(click_data),
    )

    session.add(anonymous_click)
    await session.commit()

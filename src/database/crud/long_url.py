from datetime import datetime, timezone

from sqlalchemy import select

from ..db_config import AsyncSessionDep
from ..models import ShortURL


async def get_long_url_by_slug_from_db(slug: str, session: AsyncSessionDep) -> str | None:
    """ """
    # query = select(ShortURL).where(ShortURL.slug==slug)
    query = select(ShortURL).filter_by(slug=slug)
    short_url: ShortURL | None = (await session.execute(query)).scalar_one_or_none()

    if short_url:
        short_url.click_count += 1
        short_url.last_accessed_at = datetime.now(timezone.utc)
        await session.commit()
        return short_url.long_url

    return None

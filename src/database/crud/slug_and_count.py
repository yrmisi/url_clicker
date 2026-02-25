from sqlalchemy import select

from src.utils import SlugCountInfo

from ..db_config import AsyncSessionDep
from ..models import ShortURL


async def get_slug_and_count_by_long_url_from_db(
    long_url: str,
    session: AsyncSessionDep,
) -> SlugCountInfo | None:
    """ """
    query = select(ShortURL).filter_by(long_url=long_url)
    short_url: ShortURL | None = (await session.execute(query)).scalar_one_or_none()

    if short_url:
        short_url.creation_count += 1
        await session.commit()
        return SlugCountInfo(
            slug=short_url.slug,
            creation_count=short_url.creation_count,
        )

    return None

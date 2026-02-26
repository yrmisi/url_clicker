from database import AsyncSessionDep
from database.crud import get_long_url_by_slug_db
from exceptions import NoLongFoundError


async def get_long_url(slug: str, session: AsyncSessionDep) -> str:
    """ """
    long_url: str | None = await get_long_url_by_slug_db(slug, session)
    if long_url is None:
        raise NoLongFoundError()
    return long_url

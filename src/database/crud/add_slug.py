from sqlalchemy.exc import IntegrityError

from src.dependencies import ClickDataDep
from src.exceptions import SlugAlreadyExistsDBError

from ..dependencies import AsyncSessionDep
from ..models import ShortURL
from .anonymous_click import add_anonymous_click_db


async def add_slug_db(
    slug: str,
    long_url: str,
    click_data: ClickDataDep,
    session: AsyncSessionDep,
) -> None:
    """ """
    short_url: ShortURL = ShortURL(slug=slug, long_url=long_url)
    session.add(short_url)
    try:
        await session.commit()
        await add_anonymous_click_db(short_url.id, click_data, session)
    except IntegrityError:
        raise SlugAlreadyExistsDBError

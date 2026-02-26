from database import AsyncSessionDep
from database.crud import add_slug_db, get_slug_and_count_by_long_url_db
from dependencies import ClickDataDep
from exceptions import InvalidURLError, SlugAlreadyExistsDBError
from schemas import SlugCountInfo
from utils import generate_slug, is_valid_url


async def get_slug(
    url: str,
    click_data: ClickDataDep,
    session: AsyncSessionDep,
) -> SlugCountInfo:
    """ """
    cleaned_url = url.strip().rstrip("/")

    if not is_valid_url(cleaned_url):
        raise InvalidURLError()

    slug_count: SlugCountInfo | None = await get_slug_and_count_by_long_url_db(
        cleaned_url,
        session,
    )
    if slug_count:
        return slug_count

    slug: str = generate_slug()
    try:
        await add_slug_db(slug, cleaned_url, click_data, session)
    except SlugAlreadyExistsDBError as exc:
        raise exc
    return SlugCountInfo(slug=slug, creation_count=1)

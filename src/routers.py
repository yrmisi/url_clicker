from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from config import settings
from database import AsyncSessionDep
from dependencies import ClickDataDep, rate_limit_short_url
from exceptions import InvalidURLError, NoLongFoundError, SlugAlreadyExistsDBError
from schemas import ShortUrlResponse, SlugCountInfo
from services import get_long_url, get_slug

router_slug: APIRouter = APIRouter()


@router_slug.post(
    "/short_url",
    response_model=ShortUrlResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit_short_url)],
)
async def generate_slug(
    long_url: Annotated[str, Body(embed=True)],
    click_data: ClickDataDep,
    session: AsyncSessionDep,
) -> dict[str, str | int]:
    """The router receives the website address, generates and returns a short link."""
    for attempt in range(5):
        try:
            slug_count: SlugCountInfo = await get_slug(long_url, click_data, session)
            return settings.app.get_link_count(**asdict(slug_count))
        except SlugAlreadyExistsDBError:
            if attempt == 4:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to generate unique slug after 5 attempts",
                )
        except InvalidURLError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="invalid URL",
            )
    # Этот код недостижим, но успокаивает Pylance
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unexpected error",
    )


@router_slug.get("/{slug}")
async def redirect_to_url(slug: str, session: AsyncSessionDep) -> RedirectResponse:
    """ """
    try:
        url: str = await get_long_url(slug, session)
    except NoLongFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The link does not exist")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from config import settings
from core import templates, translations_cache
from database import AsyncSessionDep
from dependencies import ClickDataDep, LanguageDep, rate_limit_short_url
from exceptions import InvalidURLError, NoLongFoundError, SlugAlreadyExistsDBError
from schemas import SlugCountInfo
from services import get_long_url, get_slug

router = APIRouter(tags=["Shortener"])


@router.post(
    "/short_url",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit_short_url)],
)
async def generate_slug(
    long_url: Annotated[str, Body(embed=True)],
    click_data: ClickDataDep,
    session: AsyncSessionDep,
    lang: LanguageDep,
    request: Request,
    html: Annotated[bool, Query()] = False,
) -> HTMLResponse | dict[str, str | int]:
    """The router receives the website address, generates and returns a short link."""
    for attempt in range(5):
        try:
            slug_count: SlugCountInfo = await get_slug(long_url, click_data, session)
            data_link: dict[str, int | str] = settings.app.get_link_count(**asdict(slug_count))

            if html:
                ctx: dict[str, str] = translations_cache.get(lang, translations_cache["en"]).copy()
                ctx["times_generated"] = ctx["times_generated"].format(
                    creation_count=data_link["creation_count"]
                )
                ctx["data_short_url"] = str(data_link["link"])

                return templates.TemplateResponse(
                    request=request,
                    name="result.html",
                    context=ctx,
                )
            return data_link
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


@router.get("/{slug}")
async def redirect_to_url(slug: str, session: AsyncSessionDep) -> RedirectResponse:
    """ """
    try:
        url: str = await get_long_url(slug, session)
    except NoLongFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The link does not exist")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

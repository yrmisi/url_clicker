from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from core import templates, translations_cache
from dependencies import LanguageDep

router = APIRouter(tags=["System "])


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, lang: LanguageDep) -> HTMLResponse:
    """Render the localized start page using the requested language."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=translations_cache.get(lang),
    )

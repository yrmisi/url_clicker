from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from core import templates, translations_cache
from utils import get_preferred_language

router = APIRouter(tags=["System "])


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Start page."""
    lang = get_preferred_language(request)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=translations_cache.get(lang),
    )

from typing import Annotated

from fastapi import Depends, Request


def get_preferred_language(request: Request) -> str:
    """Determines the user's language."""
    accept_lang: str = request.headers.get("accept-language", "en").lower()
    return "ru" if accept_lang.startswith("ru") else "en"


LanguageDep = Annotated[str, Depends(get_preferred_language)]

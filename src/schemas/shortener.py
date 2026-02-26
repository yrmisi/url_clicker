from pydantic import BaseModel, HttpUrl


class ShortUrlResponse(BaseModel):
    """Router data return scheme."""

    link: HttpUrl
    creation_count: int

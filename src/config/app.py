from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .path import BASE_DIR


class AppConfig(BaseSettings):
    """Basic application settings."""

    scheme: Annotated[str, Field(alias="SCHEME")] = "http"
    domain: Annotated[str, Field(alias="DOMAIN")] = "localhost"
    api_prefix: Annotated[str, Field(alias="API_PREFIX")] = "/api"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / "envs" / ".env.appdev",
        env_file_encoding="utf-8",
    )

    @property
    def base_url(self) -> str:
        """Full base URL with scheme."""
        return f"{self.scheme}://{self.domain}"

    def get_link_count(self, slug: str, creation_count: int) -> dict[str, str | int]:
        """Generates and returns a response in the form of a dictionary."""
        return {
            "link": f"{self.base_url}{self.api_prefix}/{slug}",
            "creation_count": creation_count,
        }

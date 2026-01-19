"""Configuration for the Porkbun MCP server."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PorkbunMCPSettings(BaseSettings):
    """Configuration for the Porkbun MCP server.

    Attributes:
        api_key: Porkbun API key (pk1_...).
        secret_key: Porkbun secret API key (sk1_...).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PORKBUN_",
        extra="ignore",
    )

    api_key: str = Field(default="", description="Porkbun API key")
    secret_key: str = Field(default="", description="Porkbun secret key")
    get_muddy: bool = Field(
        default=False,
        description="Enable write operations (create/edit/delete). Default is read-only.",
    )

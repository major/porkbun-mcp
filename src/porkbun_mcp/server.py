"""FastMCP server setup and lifespan management."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from fastmcp import FastMCP
from oinker import AsyncPiglet

from porkbun_mcp.config import PorkbunMCPSettings


@dataclass
class AppContext:
    """Typed application context for lifespan-managed resources."""

    piglet: AsyncPiglet
    read_only: bool


@asynccontextmanager
async def lifespan(mcp: "FastMCP") -> AsyncIterator[AppContext]:
    """Manage AsyncPiglet client lifecycle."""
    settings = PorkbunMCPSettings()

    # CLI override takes precedence over environment variable
    get_muddy_override = getattr(mcp, "_get_muddy_override", None)
    get_muddy = get_muddy_override if get_muddy_override is not None else settings.get_muddy
    read_only = not get_muddy

    async with AsyncPiglet(
        api_key=settings.api_key,
        secret_key=settings.secret_key,
    ) as piglet:
        yield AppContext(piglet=piglet, read_only=read_only)


def create_server(get_muddy: bool | None = None) -> FastMCP:
    """Create and configure the MCP server.

    Args:
        get_muddy: Enable write operations. If None, uses PORKBUN_GET_MUDDY env var.
    """
    mcp = FastMCP(
        name="porkbun",
        instructions="""Porkbun DNS management.

Tool selection:
- *_by_name_type variants: Use when you know subdomain+type but not record ID
- *_by_id variants: Use when you have the record ID from a previous list/get
""",
        lifespan=lifespan,
    )

    from porkbun_mcp.prompts import register_prompts
    from porkbun_mcp.tools import register_tools

    register_tools(mcp)
    register_prompts(mcp)

    if get_muddy is not None:
        mcp._get_muddy_override = get_muddy  # type: ignore[attr-defined]

    return mcp

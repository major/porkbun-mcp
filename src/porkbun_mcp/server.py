"""FastMCP server setup and lifespan management."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastmcp import FastMCP
from oinker import AsyncPiglet

from porkbun_mcp.config import PorkbunMCPSettings


@asynccontextmanager
async def lifespan(mcp: FastMCP) -> AsyncIterator[dict[str, Any]]:
    """Manage AsyncPiglet client lifecycle."""
    settings = PorkbunMCPSettings()

    async with AsyncPiglet(
        api_key=settings.api_key,
        secret_key=settings.secret_key,
    ) as piglet:
        yield {"piglet": piglet}


def create_server() -> FastMCP:
    """Create and configure the MCP server."""
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
    from porkbun_mcp.resources import register_resources
    from porkbun_mcp.tools import register_tools

    register_tools(mcp)
    register_resources(mcp)
    register_prompts(mcp)

    return mcp

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
    """Manage AsyncPiglet client lifecycle.

    Creates an AsyncPiglet client for the duration of the server's lifetime,
    making it available to all tools and resources via the context.

    Args:
        mcp: The FastMCP server instance.

    Yields:
        Context dict with piglet client and settings.
    """
    settings = PorkbunMCPSettings()

    async with AsyncPiglet(
        api_key=settings.api_key,
        secret_key=settings.secret_key,
    ) as piglet:
        yield {
            "piglet": piglet,
            "settings": settings,
        }


def create_server() -> FastMCP:
    """Create and configure the MCP server.

    Returns:
        Configured FastMCP server instance.
    """
    settings = PorkbunMCPSettings()

    mode_desc = (
        "Write operations ENABLED (--get-muddy)"
        if settings.get_muddy
        else "Read-only mode (use --get-muddy for write operations)"
    )

    mcp = FastMCP(
        name="porkbun",
        instructions=f"""Porkbun DNS MCP Server

{mode_desc}

Manage DNS records and domains on Porkbun. Use tools for specific operations
or browse resources for read-only data access.

Resources:
- porkbun://domains - List all domains
- porkbun://dns/{{domain}} - DNS records for a domain
- porkbun://ssl/{{domain}} - SSL certificate bundle
- porkbun://pricing - TLD pricing
""",
        lifespan=lifespan,
    )

    from porkbun_mcp.prompts import register_prompts
    from porkbun_mcp.resources import register_resources
    from porkbun_mcp.tools import register_tools

    register_tools(mcp, settings)
    register_resources(mcp)
    register_prompts(mcp)

    return mcp

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
        instructions=f"""Porkbun DNS MCP Server - {mode_desc}

## Quick Start
Use prompts for guided workflows, or tools for specific operations.

## Common Workflows

### View/List Operations
- domains_list: See all your domains
- dns_list(domain): View all DNS records for a domain
- dns_get_by_name_type(domain, type, subdomain): Find specific records

### DNS Record Management {"(ENABLED)" if settings.get_muddy else "(requires --get-muddy)"}
- dns_create: Add new A, AAAA, MX, TXT, CNAME, etc.
- dns_edit_by_name_type: Update records by subdomain+type (easiest)
- dns_edit: Update by record ID (when you have the ID)
- dns_delete_by_name_type: Delete by subdomain+type
- dns_delete: Delete by record ID

### Common Tasks
- Point www to IP: dns_create(domain, "A", "1.2.3.4", name="www")
- Update root A record: dns_edit_by_name_type(domain, "A", content="new-ip")
- Add TXT record: dns_create(domain, "TXT", "v=spf1 include:...")

## Resources (read-only browsing)
- porkbun://domains - All domains
- porkbun://dns/{{domain}} - DNS records
- porkbun://ssl/{{domain}} - SSL certificate bundle
- porkbun://pricing - TLD pricing

## Advanced Tools
DNSSEC, glue records, and URL forwards are for specialized use cases.
Use dnssec_*, domains_*_glue_record, or domains_*_url_forward only when needed.
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

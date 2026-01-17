"""Resource registration for the Porkbun MCP server."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_resources(mcp: FastMCP) -> None:
    """Register all resources with the MCP server.

    Args:
        mcp: The FastMCP server instance.
    """
    from porkbun_mcp.resources.dns import register_dns_resources
    from porkbun_mcp.resources.domains import register_domain_resources
    from porkbun_mcp.resources.pricing import register_pricing_resources
    from porkbun_mcp.resources.ssl import register_ssl_resources

    register_domain_resources(mcp)
    register_dns_resources(mcp)
    register_ssl_resources(mcp)
    register_pricing_resources(mcp)

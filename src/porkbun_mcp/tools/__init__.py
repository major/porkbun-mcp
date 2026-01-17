"""Tool registration for the Porkbun MCP server."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastmcp import FastMCP

    from porkbun_mcp.config import PorkbunMCPSettings


def register_tools(mcp: FastMCP, settings: PorkbunMCPSettings) -> None:
    """Register all tools with the MCP server.

    Args:
        mcp: The FastMCP server instance.
        settings: Server configuration.
    """
    from porkbun_mcp.tools.dns import register_dns_tools
    from porkbun_mcp.tools.dnssec import register_dnssec_tools
    from porkbun_mcp.tools.domains import register_domain_tools
    from porkbun_mcp.tools.ping import register_ping_tools
    from porkbun_mcp.tools.pricing import register_pricing_tools
    from porkbun_mcp.tools.ssl import register_ssl_tools

    register_ping_tools(mcp)
    register_dns_tools(mcp, settings)
    register_domain_tools(mcp, settings)
    register_dnssec_tools(mcp, settings)
    register_ssl_tools(mcp)
    register_pricing_tools(mcp)

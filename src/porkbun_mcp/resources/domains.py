"""Domain resources for the Porkbun MCP server."""

from typing import TYPE_CHECKING

from fastmcp import Context

from porkbun_mcp.context import get_piglet
from porkbun_mcp.errors import handle_oinker_error
from porkbun_mcp.models import DomainInfo
from porkbun_mcp.tools.domains import _to_domain_info

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_domain_resources(mcp: FastMCP) -> None:
    """Register domain resources with the MCP server."""

    @mcp.resource("porkbun://domains")
    async def domains_resource(ctx: Context) -> list[DomainInfo]:
        """List all domains in your Porkbun account."""
        piglet = get_piglet(ctx)

        try:
            domains = await piglet.domains.list()
            return [_to_domain_info(d) for d in domains]
        except Exception as e:
            raise handle_oinker_error(e, "list domains") from e

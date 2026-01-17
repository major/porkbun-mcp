"""SSL resources for the Porkbun MCP server."""

from typing import TYPE_CHECKING

from fastmcp import Context

from porkbun_mcp.context import get_piglet
from porkbun_mcp.errors import handle_oinker_error
from porkbun_mcp.models import SSLBundle
from porkbun_mcp.tools.ssl import _to_ssl_bundle

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_ssl_resources(mcp: FastMCP) -> None:
    """Register SSL resources with the MCP server."""

    @mcp.resource("porkbun://ssl/{domain}")
    async def ssl_resource(ctx: Context, domain: str) -> SSLBundle:
        """Get SSL certificate bundle for a domain."""
        piglet = get_piglet(ctx)

        try:
            bundle = await piglet.ssl.retrieve(domain)
            return _to_ssl_bundle(bundle)
        except Exception as e:
            raise handle_oinker_error(e, f"retrieve SSL bundle for {domain}") from e

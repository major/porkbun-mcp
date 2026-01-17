"""DNS resources for the Porkbun MCP server."""

from typing import TYPE_CHECKING

from fastmcp import Context

from porkbun_mcp.context import get_piglet
from porkbun_mcp.errors import handle_oinker_error
from porkbun_mcp.models import DNSRecord
from porkbun_mcp.tools.dns import _to_dns_record

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_dns_resources(mcp: FastMCP) -> None:
    """Register DNS resources with the MCP server."""

    @mcp.resource("porkbun://dns/{domain}")
    async def dns_resource(ctx: Context, domain: str) -> list[DNSRecord]:
        """List all DNS records for a domain."""
        piglet = get_piglet(ctx)

        try:
            records = await piglet.dns.list(domain)
            return [_to_dns_record(r) for r in records]
        except Exception as e:
            raise handle_oinker_error(e, f"list DNS records for {domain}") from e

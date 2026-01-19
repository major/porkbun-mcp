"""Pricing resources for the Porkbun MCP server."""

from typing import TYPE_CHECKING

from fastmcp import Context
from oinker.pricing import get_pricing

from porkbun_mcp.errors import handle_oinker_error
from porkbun_mcp.models import TLDPricing
from porkbun_mcp.tools.pricing import _to_tld_pricing

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_pricing_resources(mcp: FastMCP) -> None:
    """Register pricing resources with the MCP server."""

    @mcp.resource("porkbun://pricing", annotations={"readOnlyHint": True})
    async def pricing_resource(ctx: Context) -> list[TLDPricing]:  # noqa: ARG001
        """Get pricing for all available TLDs."""
        try:
            pricing_dict = await get_pricing()
            return [_to_tld_pricing(tld, p) for tld, p in pricing_dict.items()]
        except Exception as e:
            raise handle_oinker_error(e, "get TLD pricing") from e

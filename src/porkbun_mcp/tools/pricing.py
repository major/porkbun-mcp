"""TLD pricing tools for the Porkbun MCP server."""

from typing import TYPE_CHECKING, Any

from fastmcp import Context
from oinker.pricing import get_pricing

from porkbun_mcp.errors import handle_oinker_error
from porkbun_mcp.models import TLDPricing

if TYPE_CHECKING:
    from fastmcp import FastMCP


def _to_tld_pricing(tld: str, p: Any) -> TLDPricing:
    """Convert oinker pricing entry to Pydantic model."""
    return TLDPricing(
        tld=tld,
        registration=p.registration,
        renewal=p.renewal,
        transfer=p.transfer,
    )


def register_pricing_tools(mcp: "FastMCP") -> None:
    """Register pricing tools with the MCP server."""

    @mcp.tool(annotations={"readOnlyHint": True})
    async def pricing_get(ctx: Context) -> list[TLDPricing]:  # noqa: ARG001
        """Get pricing for all available TLDs.

        PREFERRED for price lookups - no rate limits, returns all TLD prices at once.
        Use this FIRST when users ask about domain costs, then filter by TLD.
        Only use domains_check_availability when you need to verify a specific
        domain is actually available for purchase.
        """
        try:
            pricing_dict = await get_pricing()
            return [_to_tld_pricing(tld, p) for tld, p in pricing_dict.items()]
        except Exception as e:
            raise handle_oinker_error(e, "get TLD pricing") from e

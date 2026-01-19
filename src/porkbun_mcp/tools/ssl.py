"""SSL certificate tools for the Porkbun MCP server."""

from typing import TYPE_CHECKING, Annotated, Any

from fastmcp import Context
from pydantic import Field

from porkbun_mcp.context import get_piglet
from porkbun_mcp.errors import handle_oinker_error
from porkbun_mcp.models import SSLBundle

if TYPE_CHECKING:
    from fastmcp import FastMCP


def _to_ssl_bundle(bundle: Any) -> SSLBundle:
    """Convert oinker SSL bundle to Pydantic model."""
    return SSLBundle(
        certificate_chain=bundle.certificate_chain,
        private_key=bundle.private_key,
        public_key=bundle.public_key,
    )


def register_ssl_tools(mcp: "FastMCP") -> None:
    """Register SSL tools with the MCP server."""

    @mcp.tool(annotations={"readOnlyHint": True})
    async def ssl_retrieve(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
    ) -> SSLBundle:
        """Retrieve the SSL certificate bundle for a domain.

        Only available for domains using Porkbun nameservers.
        """
        piglet = get_piglet(ctx)

        try:
            bundle = await piglet.ssl.retrieve(domain)
            return _to_ssl_bundle(bundle)
        except Exception as e:
            raise handle_oinker_error(e, f"retrieve SSL bundle for {domain}") from e

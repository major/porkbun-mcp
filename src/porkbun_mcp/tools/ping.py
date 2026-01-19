"""Ping tool for testing API connectivity."""

from typing import TYPE_CHECKING

from fastmcp import Context

from porkbun_mcp.context import get_piglet
from porkbun_mcp.errors import handle_oinker_error
from porkbun_mcp.models import PingResult

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_ping_tools(mcp: "FastMCP") -> None:
    """Register ping tools with the MCP server."""

    @mcp.tool(annotations={"readOnlyHint": True})
    async def ping(ctx: Context) -> PingResult:
        """Test API connectivity and get your public IP address."""
        piglet = get_piglet(ctx)

        try:
            result = await piglet.ping()
            return PingResult(status="SUCCESS", your_ip=result.your_ip)
        except Exception as e:
            raise handle_oinker_error(e, "ping API") from e

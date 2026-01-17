"""Context helpers for safe lifespan context access."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastmcp import Context
from fastmcp.exceptions import ToolError

if TYPE_CHECKING:
    from oinker import AsyncPiglet

    from porkbun_mcp.config import PorkbunMCPSettings


def get_piglet(ctx: Context) -> AsyncPiglet:
    """Get AsyncPiglet from context.

    Args:
        ctx: MCP context.

    Returns:
        The AsyncPiglet client.

    Raises:
        ToolError: If context is not available.
    """
    if ctx.request_context is None or ctx.request_context.lifespan_context is None:
        raise ToolError("Server context not available")
    return ctx.request_context.lifespan_context["piglet"]


def get_settings(ctx: Context) -> PorkbunMCPSettings:
    """Get settings from context.

    Args:
        ctx: MCP context.

    Returns:
        The PorkbunMCPSettings.

    Raises:
        ToolError: If context is not available.
    """
    if ctx.request_context is None or ctx.request_context.lifespan_context is None:
        raise ToolError("Server context not available")
    return ctx.request_context.lifespan_context["settings"]


def require_write_mode(ctx: Context) -> None:
    """Ensure write operations are enabled, or raise ToolError.

    Call this at the start of any tool that modifies data.

    Args:
        ctx: MCP context.

    Raises:
        ToolError: If --get-muddy mode is not enabled.
    """
    settings = get_settings(ctx)
    if not settings.get_muddy:
        raise ToolError(
            "Write operations require --get-muddy mode. "
            "Restart with PORKBUN_GET_MUDDY=true or --get-muddy flag."
        )

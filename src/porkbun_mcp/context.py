"""Context helpers for safe lifespan context access."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastmcp import Context
from fastmcp.exceptions import ToolError

if TYPE_CHECKING:
    from oinker import AsyncPiglet

    from porkbun_mcp.server import AppContext


def get_piglet(ctx: Context[object, AppContext]) -> AsyncPiglet:
    """Get AsyncPiglet from context."""
    if ctx.request_context is None or ctx.request_context.lifespan_context is None:
        raise ToolError("Server context not available")
    return ctx.request_context.lifespan_context.piglet


def get_read_only(ctx: Context[object, AppContext]) -> bool:
    """Check if server is in read-only mode."""
    if ctx.request_context is None or ctx.request_context.lifespan_context is None:
        return True
    return ctx.request_context.lifespan_context.read_only


def require_writes(ctx: Context[object, AppContext]) -> None:
    """Raise ToolError if server is in read-only mode."""
    if get_read_only(ctx):
        raise ToolError(
            "Write operations are disabled (read-only mode). "
            "To enable changes, set PORKBUN_GET_MUDDY=true or run with --get-muddy."
        )

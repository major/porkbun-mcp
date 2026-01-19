"""Context helpers for safe lifespan context access."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastmcp import Context
from fastmcp.exceptions import ToolError

if TYPE_CHECKING:
    from oinker import AsyncPiglet


def get_piglet(ctx: Context) -> AsyncPiglet:
    """Get AsyncPiglet from context."""
    if ctx.request_context is None or ctx.request_context.lifespan_context is None:
        raise ToolError("Server context not available")
    return ctx.request_context.lifespan_context["piglet"]

"""Error mapping from oinker to MCP ToolErrors."""

from __future__ import annotations

from fastmcp.exceptions import ToolError
from oinker import (
    APIError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


def handle_oinker_error(e: Exception, operation: str) -> ToolError:
    """Convert oinker exceptions to MCP ToolErrors.

    Args:
        e: The exception to convert.
        operation: Description of the operation that failed.

    Returns:
        A ToolError with an appropriate message.
    """
    match e:
        case AuthenticationError():
            return ToolError(
                "Authentication failed. Check PORKBUN_API_KEY and PORKBUN_SECRET_KEY.",
            )
        case AuthorizationError():
            return ToolError(
                f"Not authorized to {operation}. Ensure API access is enabled for this domain.",
            )
        case NotFoundError():
            return ToolError(f"Not found: {e}")
        case RateLimitError() as rle:
            retry_msg = f" Retry in {rle.retry_after}s." if rle.retry_after else ""
            return ToolError(f"Rate limited.{retry_msg}")
        case ValidationError():
            return ToolError(f"Validation error: {e}")
        case APIError() as ae:
            return ToolError(f"Porkbun API error: {ae.message}")
        case _:
            return ToolError(f"Error during {operation}: {e}")

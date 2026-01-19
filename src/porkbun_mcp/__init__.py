"""Porkbun MCP Server - DNS management via Model Context Protocol."""

from __future__ import annotations

import argparse


def main() -> None:
    """Run the Porkbun MCP server."""
    parser = argparse.ArgumentParser(
        description="Porkbun DNS MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  PORKBUN_API_KEY       Porkbun API key (required)
  PORKBUN_SECRET_KEY    Porkbun secret key (required)
  PORKBUN_GET_MUDDY     Enable write operations (default: false)

Examples:
  porkbun-mcp                    # Read-only mode (default)
  porkbun-mcp --get-muddy        # Enable write operations
  porkbun-mcp --transport sse    # SSE transport
""",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport protocol (default: stdio)",
    )
    parser.add_argument(
        "--get-muddy",
        action="store_true",
        default=None,
        help="Enable write operations (create/edit/delete). Default is read-only.",
    )
    args = parser.parse_args()

    from porkbun_mcp.server import create_server

    server = create_server(get_muddy=args.get_muddy)
    server.run(transport=args.transport)


__all__ = ["main"]

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

Examples:
  porkbun-mcp
  porkbun-mcp --transport sse
""",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport protocol (default: stdio)",
    )
    args = parser.parse_args()

    from porkbun_mcp.server import create_server

    server = create_server()
    server.run(transport=args.transport)


__all__ = ["main"]

"""Prompt templates for guiding LLM interactions with Porkbun DNS."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_prompts(mcp: "FastMCP") -> None:
    """Register all prompt templates with the MCP server.

    Args:
        mcp: The FastMCP server instance.
    """
    from porkbun_mcp.prompts.dns import register_dns_prompts

    register_dns_prompts(mcp)

"""Smoke tests for porkbun-mcp server integration.

These tests verify the server starts correctly and responds to MCP protocol
requests. They use FastMCPTransport for in-memory testing without network IO.
"""

from __future__ import annotations

import pytest
from fastmcp import Client
from fastmcp.client.transports import FastMCPTransport

from porkbun_mcp.server import create_server


class TestServerInitialization:
    """Smoke tests for server startup and tool registration."""

    async def test_server_creates_successfully(self) -> None:
        """Server can be created without errors."""
        server = create_server()
        assert server is not None
        assert server.name == "porkbun"

    async def test_server_lists_tools(self) -> None:
        """Server lists expected tools via MCP protocol."""
        server = create_server()

        async with Client(FastMCPTransport(server)) as client:
            tools = await client.list_tools()
            tool_names = [t.name for t in tools]

            assert "ping" in tool_names
            assert "dns_list" in tool_names
            assert "dns_create" in tool_names
            assert "domains_list" in tool_names
            assert "pricing_get" in tool_names

    async def test_server_lists_resources(self) -> None:
        """Server lists expected resources via MCP protocol."""
        server = create_server()

        async with Client(FastMCPTransport(server)) as client:
            resources = await client.list_resources()
            resource_uris = [str(r.uri) for r in resources]

            assert any("domains" in uri for uri in resource_uris)
            assert any("pricing" in uri for uri in resource_uris)


class TestReadOnlyModeIntegration:
    """Smoke tests for read-only mode via MCP protocol."""

    async def test_write_tool_blocked_by_default(self) -> None:
        """Write tools return error in default read-only mode."""
        server = create_server()

        async with Client(FastMCPTransport(server)) as client:
            result = await client.call_tool(
                "dns_create",
                {"domain": "example.com", "record_type": "A", "content": "192.0.2.1"},
                raise_on_error=False,
            )

            assert result.is_error
            error_text = str(result.content[0].text).lower()
            assert "read-only" in error_text
            assert "get-muddy" in error_text

    async def test_write_tool_allowed_with_get_muddy(self) -> None:
        """Write tools proceed (may fail at API) when get_muddy=True."""
        server = create_server(get_muddy=True)

        async with Client(FastMCPTransport(server)) as client:
            result = await client.call_tool(
                "dns_create",
                {"domain": "example.com", "record_type": "A", "content": "192.0.2.1"},
                raise_on_error=False,
            )

            if result.is_error:
                error_text = str(result.content[0].text).lower()
                assert "read-only" not in error_text


@pytest.mark.network
class TestPricingEndpoint:
    """Smoke tests that make real network calls to public endpoints.

    These tests are marked with @pytest.mark.network and can be skipped
    in environments without network access using: pytest -m "not network"
    """

    async def test_pricing_get_returns_data(self) -> None:
        """pricing_get returns TLD pricing from Porkbun API (no auth required)."""
        server = create_server()

        async with Client(FastMCPTransport(server)) as client:
            result = await client.call_tool("pricing_get", {})

            assert not result.is_error
            assert result.content
            assert len(result.content) > 0

"""Tests for read-only mode enforcement."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from conftest import get_tool_fn
from porkbun_mcp.context import get_read_only, require_writes
from porkbun_mcp.server import AppContext
from porkbun_mcp.tools.dns import register_dns_tools
from porkbun_mcp.tools.dnssec import register_dnssec_tools
from porkbun_mcp.tools.domains import register_domain_tools


@pytest.fixture
def read_only_context(mock_piglet: AsyncMock) -> MagicMock:
    """Context in read-only mode."""
    ctx = MagicMock()
    ctx.request_context = MagicMock()
    ctx.request_context.lifespan_context = AppContext(piglet=mock_piglet, read_only=True)
    return ctx


class TestRequireWrites:
    """Tests for require_writes helper."""

    def test_raises_when_read_only(self, read_only_context: MagicMock) -> None:
        """require_writes raises ToolError when read_only=True."""
        with pytest.raises(ToolError, match="read-only"):
            require_writes(read_only_context)

    def test_error_mentions_get_muddy(self, read_only_context: MagicMock) -> None:
        """Error message tells user how to enable writes."""
        with pytest.raises(ToolError, match="get-muddy"):
            require_writes(read_only_context)

    def test_passes_when_writes_enabled(
        self, mock_piglet: AsyncMock, mock_context: MagicMock
    ) -> None:
        """require_writes does not raise when read_only=False."""
        require_writes(mock_context)

    def test_get_read_only_returns_true_when_read_only(self, read_only_context: MagicMock) -> None:
        """get_read_only returns True in read-only mode."""
        assert get_read_only(read_only_context) is True

    def test_get_read_only_returns_false_when_writes_enabled(self, mock_context: MagicMock) -> None:
        """get_read_only returns False when writes enabled."""
        assert get_read_only(mock_context) is False

    def test_get_read_only_defaults_to_true_on_missing_context(self) -> None:
        """get_read_only returns True (safe default) if context unavailable."""
        ctx = MagicMock()
        ctx.request_context = None
        assert get_read_only(ctx) is True


class TestDNSWriteToolsBlocked:
    """Tests that DNS write tools are blocked in read-only mode."""

    async def test_dns_create_blocked(self, read_only_context: MagicMock) -> None:
        """dns_create raises ToolError in read-only mode."""
        mcp = FastMCP("test")
        register_dns_tools(mcp)
        tool_fn = get_tool_fn(mcp, "dns_create")

        with pytest.raises(ToolError, match="read-only"):
            await tool_fn(
                read_only_context,
                domain="example.com",
                record_type="A",
                content="192.0.2.1",
            )

    async def test_dns_edit_blocked(self, read_only_context: MagicMock) -> None:
        """dns_edit raises ToolError in read-only mode."""
        mcp = FastMCP("test")
        register_dns_tools(mcp)
        tool_fn = get_tool_fn(mcp, "dns_edit")

        with pytest.raises(ToolError, match="read-only"):
            await tool_fn(
                read_only_context,
                domain="example.com",
                record_id="123",
                record_type="A",
                content="192.0.2.1",
            )

    async def test_dns_delete_blocked(self, read_only_context: MagicMock) -> None:
        """dns_delete raises ToolError in read-only mode."""
        mcp = FastMCP("test")
        register_dns_tools(mcp)
        tool_fn = get_tool_fn(mcp, "dns_delete")

        with pytest.raises(ToolError, match="read-only"):
            await tool_fn(read_only_context, domain="example.com", record_id="123")


class TestDomainWriteToolsBlocked:
    """Tests that domain write tools are blocked in read-only mode."""

    async def test_domains_update_nameservers_blocked(self, read_only_context: MagicMock) -> None:
        """domains_update_nameservers raises ToolError in read-only mode."""
        mcp = FastMCP("test")
        register_domain_tools(mcp)
        tool_fn = get_tool_fn(mcp, "domains_update_nameservers")

        with pytest.raises(ToolError, match="read-only"):
            await tool_fn(
                read_only_context,
                domain="example.com",
                nameservers=["ns1.example.com", "ns2.example.com"],
            )

    async def test_domains_add_url_forward_blocked(self, read_only_context: MagicMock) -> None:
        """domains_add_url_forward raises ToolError in read-only mode."""
        mcp = FastMCP("test")
        register_domain_tools(mcp)
        tool_fn = get_tool_fn(mcp, "domains_add_url_forward")

        with pytest.raises(ToolError, match="read-only"):
            await tool_fn(
                read_only_context,
                domain="example.com",
                location="https://example.org",
            )


class TestDNSSECWriteToolsBlocked:
    """Tests that DNSSEC write tools are blocked in read-only mode."""

    async def test_dnssec_create_blocked(self, read_only_context: MagicMock) -> None:
        """dnssec_create raises ToolError in read-only mode."""
        mcp = FastMCP("test")
        register_dnssec_tools(mcp)
        tool_fn = get_tool_fn(mcp, "dnssec_create")

        with pytest.raises(ToolError, match="read-only"):
            await tool_fn(
                read_only_context,
                domain="example.com",
                key_tag="12345",
                algorithm="13",
                digest_type="2",
                digest="abc123",
            )

    async def test_dnssec_delete_blocked(self, read_only_context: MagicMock) -> None:
        """dnssec_delete raises ToolError in read-only mode."""
        mcp = FastMCP("test")
        register_dnssec_tools(mcp)
        tool_fn = get_tool_fn(mcp, "dnssec_delete")

        with pytest.raises(ToolError, match="read-only"):
            await tool_fn(read_only_context, domain="example.com", key_tag="12345")


class TestReadToolsAlwaysWork:
    """Tests that read-only tools work regardless of mode."""

    async def test_dns_list_works_in_read_only(
        self, read_only_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """dns_list works in read-only mode."""
        mock_piglet.dns.list.return_value = []
        mcp = FastMCP("test")
        register_dns_tools(mcp)
        tool_fn = get_tool_fn(mcp, "dns_list")

        result = await tool_fn(read_only_context, domain="example.com")
        assert result == []

    async def test_domains_list_works_in_read_only(
        self, read_only_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_list works in read-only mode."""
        mock_piglet.domains.list.return_value = []
        mcp = FastMCP("test")
        register_domain_tools(mcp)
        tool_fn = get_tool_fn(mcp, "domains_list")

        result = await tool_fn(read_only_context)
        assert result == []

    async def test_dnssec_list_works_in_read_only(
        self, read_only_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """dnssec_list works in read-only mode."""
        mock_piglet.dnssec.list.return_value = []
        mcp = FastMCP("test")
        register_dnssec_tools(mcp)
        tool_fn = get_tool_fn(mcp, "dnssec_list")

        result = await tool_fn(read_only_context, domain="example.com")
        assert result == []

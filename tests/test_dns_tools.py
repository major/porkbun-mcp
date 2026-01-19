"""Tests for DNS tools."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from conftest import get_tool_fn, make_mock_dns_record
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from porkbun_mcp.models import DNSRecord, DNSRecordCreated, DNSRecordDeleted
from porkbun_mcp.tools.dns import register_dns_tools


def _register_dns() -> FastMCP:
    mcp = FastMCP("test")
    register_dns_tools(mcp)
    return mcp


class TestDNSList:
    """Tests for dns_list tool."""

    async def test_dns_list_returns_records(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """dns_list should return list of DNSRecord models."""
        mock_piglet.dns.list.return_value = [make_mock_dns_record()]
        mcp = _register_dns()
        tool_fn = get_tool_fn(mcp, "dns_list")

        result = await tool_fn(mock_context, domain="example.com")

        assert len(result) == 1
        assert isinstance(result[0], DNSRecord)
        assert result[0].id == "12345"
        assert result[0].type == "A"
        assert result[0].name == "www.example.com"
        mock_piglet.dns.list.assert_called_once_with("example.com")

    async def test_dns_list_empty(self, mock_context: MagicMock, mock_piglet: AsyncMock) -> None:
        """dns_list should return empty list when no records."""
        mock_piglet.dns.list.return_value = []
        mcp = _register_dns()
        tool_fn = get_tool_fn(mcp, "dns_list")

        result = await tool_fn(mock_context, domain="example.com")

        assert result == []


class TestDNSGet:
    """Tests for dns_get tool."""

    async def test_dns_get_returns_record(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """dns_get should return a single DNSRecord."""
        mock_piglet.dns.get.return_value = make_mock_dns_record()
        mcp = _register_dns()
        tool_fn = get_tool_fn(mcp, "dns_get")

        result = await tool_fn(mock_context, domain="example.com", record_id="12345")

        assert isinstance(result, DNSRecord)
        assert result.id == "12345"

    async def test_dns_get_not_found(self, mock_context: MagicMock, mock_piglet: AsyncMock) -> None:
        """dns_get should raise ToolError when record not found."""
        mock_piglet.dns.get.return_value = None
        mcp = _register_dns()
        tool_fn = get_tool_fn(mcp, "dns_get")

        with pytest.raises(ToolError, match="not found"):
            await tool_fn(mock_context, domain="example.com", record_id="99999")


class TestDNSCreate:
    """Tests for dns_create tool."""

    async def test_dns_create_success(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """dns_create should return DNSRecordCreated on success."""
        mock_piglet.dns.create.return_value = "12345"
        mcp = _register_dns()
        tool_fn = get_tool_fn(mcp, "dns_create")

        result = await tool_fn(
            mock_context,
            domain="example.com",
            record_type="A",
            content="192.0.2.1",
        )

        assert isinstance(result, DNSRecordCreated)
        assert result.status == "created"
        assert result.record_id == "12345"

    async def test_dns_create_invalid_type(self, mock_context: MagicMock) -> None:
        """dns_create should raise ToolError for invalid record type."""
        mcp = _register_dns()
        tool_fn = get_tool_fn(mcp, "dns_create")

        with pytest.raises(ToolError, match="Unknown record type"):
            await tool_fn(
                mock_context,
                domain="example.com",
                record_type="INVALID",
                content="test",
            )


class TestDNSDelete:
    """Tests for dns_delete tool."""

    async def test_dns_delete_success(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """dns_delete should return DNSRecordDeleted on success."""
        mcp = _register_dns()
        tool_fn = get_tool_fn(mcp, "dns_delete")

        result = await tool_fn(mock_context, domain="example.com", record_id="12345")

        assert isinstance(result, DNSRecordDeleted)
        assert result.status == "deleted"
        mock_piglet.dns.delete.assert_called_once_with("example.com", "12345")

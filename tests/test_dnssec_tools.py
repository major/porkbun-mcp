"""Tests for DNSSEC tools."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

from conftest import get_tool_fn
from fastmcp import FastMCP

from porkbun_mcp.models import DNSRecordDeleted, DNSSECRecord
from porkbun_mcp.tools.dnssec import register_dnssec_tools


def _register_dnssec() -> FastMCP:
    mcp = FastMCP("test")
    register_dnssec_tools(mcp)
    return mcp


def make_mock_dnssec_record(
    key_tag: str = "12345",
    algorithm: str = "13",
    digest_type: str = "2",
    digest: str = "abc123",
) -> MagicMock:
    """Create a mock DNSSEC record."""
    record = MagicMock()
    record.key_tag = key_tag
    record.algorithm = algorithm
    record.digest_type = digest_type
    record.digest = digest
    return record


class TestDNSSECList:
    """Tests for dnssec_list tool."""

    async def test_dnssec_list_returns_records(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """dnssec_list should return list of DNSSECRecord models."""
        mock_piglet.dnssec.list.return_value = [make_mock_dnssec_record()]
        mcp = _register_dnssec()
        tool_fn = await get_tool_fn(mcp, "dnssec_list")

        result = await tool_fn(mock_context, domain="example.com")

        assert len(result) == 1
        assert isinstance(result[0], DNSSECRecord)
        assert result[0].key_tag == "12345"
        assert result[0].algorithm == "13"
        mock_piglet.dnssec.list.assert_called_once_with("example.com")

    async def test_dnssec_list_empty(self, mock_context: MagicMock, mock_piglet: AsyncMock) -> None:
        """dnssec_list should return empty list when no records."""
        mock_piglet.dnssec.list.return_value = []
        mcp = _register_dnssec()
        tool_fn = await get_tool_fn(mcp, "dnssec_list")

        result = await tool_fn(mock_context, domain="example.com")

        assert result == []


class TestDNSSECCreate:
    """Tests for dnssec_create tool."""

    async def test_dnssec_create_success(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """dnssec_create should return DNSSECRecord on success."""
        mcp = _register_dnssec()
        tool_fn = await get_tool_fn(mcp, "dnssec_create")

        result = await tool_fn(
            mock_context,
            domain="example.com",
            key_tag="12345",
            algorithm="13",
            digest_type="2",
            digest="abc123def456",
        )

        assert isinstance(result, DNSSECRecord)
        assert result.key_tag == "12345"
        assert result.algorithm == "13"
        mock_piglet.dnssec.create.assert_called_once()


class TestDNSSECDelete:
    """Tests for dnssec_delete tool."""

    async def test_dnssec_delete_success(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """dnssec_delete should return DNSRecordDeleted on success."""
        mcp = _register_dnssec()
        tool_fn = await get_tool_fn(mcp, "dnssec_delete")

        result = await tool_fn(mock_context, domain="example.com", key_tag="12345")

        assert isinstance(result, DNSRecordDeleted)
        assert result.status == "deleted"
        mock_piglet.dnssec.delete.assert_called_once_with("example.com", "12345")

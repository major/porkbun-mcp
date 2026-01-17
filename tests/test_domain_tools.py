"""Tests for domain management tools."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from conftest import get_tool_fn, make_mock_domain
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from porkbun_mcp.config import PorkbunMCPSettings
from porkbun_mcp.models import DomainAvailability, DomainInfo, Nameservers
from porkbun_mcp.tools.domains import register_domain_tools


def _register_domains_readonly() -> tuple[FastMCP, PorkbunMCPSettings]:
    mcp = FastMCP("test")
    settings = PorkbunMCPSettings(api_key="test", secret_key="test", get_muddy=False)
    register_domain_tools(mcp, settings)
    return mcp, settings


def _register_domains_write() -> tuple[FastMCP, PorkbunMCPSettings]:
    mcp = FastMCP("test")
    settings = PorkbunMCPSettings(api_key="test", secret_key="test", get_muddy=True)
    register_domain_tools(mcp, settings)
    return mcp, settings


class TestDomainsList:
    """Tests for domains_list tool."""

    async def test_domains_list_returns_domains(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_list should return list of DomainInfo models."""
        mock_piglet.domains.list.return_value = [make_mock_domain()]
        mcp, _ = _register_domains_readonly()
        tool_fn = get_tool_fn(mcp, "domains_list")

        result = await tool_fn(mock_context)

        assert len(result) == 1
        assert isinstance(result[0], DomainInfo)
        assert result[0].domain == "example.com"
        assert result[0].status == "ACTIVE"


class TestDomainsGetNameservers:
    """Tests for domains_get_nameservers tool."""

    async def test_get_nameservers_returns_list(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_get_nameservers should return Nameservers model."""
        mock_piglet.domains.get_nameservers.return_value = [
            "ns1.porkbun.com",
            "ns2.porkbun.com",
        ]
        mcp, _ = _register_domains_readonly()
        tool_fn = get_tool_fn(mcp, "domains_get_nameservers")

        result = await tool_fn(mock_context, domain="example.com")

        assert isinstance(result, Nameservers)
        assert result.domain == "example.com"
        assert len(result.nameservers) == 2


class TestDomainsUpdateNameservers:
    """Tests for domains_update_nameservers tool."""

    async def test_update_nameservers_blocked_without_get_muddy(
        self, mock_context: MagicMock
    ) -> None:
        """domains_update_nameservers should raise ToolError without --get-muddy."""
        mcp, _ = _register_domains_readonly()
        tool_fn = get_tool_fn(mcp, "domains_update_nameservers")

        with pytest.raises(ToolError, match="--get-muddy"):
            await tool_fn(
                mock_context,
                domain="example.com",
                nameservers=["ns1.example.com"],
            )

    async def test_update_nameservers_success(
        self, mock_context_write: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_update_nameservers should return updated Nameservers."""
        mcp, _ = _register_domains_write()
        tool_fn = get_tool_fn(mcp, "domains_update_nameservers")

        result = await tool_fn(
            mock_context_write,
            domain="example.com",
            nameservers=["ns1.custom.com", "ns2.custom.com"],
        )

        assert isinstance(result, Nameservers)
        assert result.nameservers == ["ns1.custom.com", "ns2.custom.com"]
        mock_piglet.domains.update_nameservers.assert_called_once()


class TestDomainsCheckAvailability:
    """Tests for domains_check_availability tool."""

    async def test_check_availability_returns_result(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_check_availability should return DomainAvailability."""
        mock_result = MagicMock()
        mock_result.available = True
        mock_result.price = "9.68"
        mock_result.premium = False
        mock_piglet.domains.check.return_value = mock_result
        mcp, _ = _register_domains_readonly()
        tool_fn = get_tool_fn(mcp, "domains_check_availability")

        result = await tool_fn(mock_context, domain="available-domain.com")

        assert isinstance(result, DomainAvailability)
        assert result.available is True
        assert result.price == "9.68"
        mock_piglet.domains.check.assert_called_once_with("available-domain.com")

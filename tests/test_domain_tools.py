"""Tests for domain management tools."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

from conftest import get_tool_fn, make_mock_domain
from fastmcp import FastMCP

from porkbun_mcp.models import (
    DomainAvailability,
    DomainInfo,
    GlueRecord,
    GlueRecordCreated,
    Nameservers,
    URLForward,
    URLForwardCreated,
)
from porkbun_mcp.tools.domains import register_domain_tools


def _register_domains() -> FastMCP:
    mcp = FastMCP("test")
    register_domain_tools(mcp)
    return mcp


class TestDomainsList:
    """Tests for domains_list tool."""

    async def test_domains_list_returns_domains(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_list should return list of DomainInfo models."""
        mock_piglet.domains.list.return_value = [make_mock_domain()]
        mcp = _register_domains()
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
        mcp = _register_domains()
        tool_fn = get_tool_fn(mcp, "domains_get_nameservers")

        result = await tool_fn(mock_context, domain="example.com")

        assert isinstance(result, Nameservers)
        assert result.domain == "example.com"
        assert len(result.nameservers) == 2


class TestDomainsUpdateNameservers:
    """Tests for domains_update_nameservers tool."""

    async def test_update_nameservers_success(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_update_nameservers should return updated Nameservers."""
        mcp = _register_domains()
        tool_fn = get_tool_fn(mcp, "domains_update_nameservers")

        result = await tool_fn(
            mock_context,
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
        mcp = _register_domains()
        tool_fn = get_tool_fn(mcp, "domains_check_availability")

        result = await tool_fn(mock_context, domain="available-domain.com")

        assert isinstance(result, DomainAvailability)
        assert result.available is True
        assert result.price == "9.68"
        mock_piglet.domains.check.assert_called_once_with("available-domain.com")


class TestDomainsGetUrlForwards:
    """Tests for domains_get_url_forwards tool."""

    async def test_get_url_forwards_returns_list(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_get_url_forwards should return list of URLForward."""
        mock_forward = MagicMock()
        mock_forward.id = "123"
        mock_forward.subdomain = "www"
        mock_forward.location = "https://example.org"
        mock_forward.type = "temporary"
        mock_forward.include_path = False
        mock_forward.wildcard = False
        mock_piglet.domains.get_url_forwards.return_value = [mock_forward]
        mcp = _register_domains()
        tool_fn = get_tool_fn(mcp, "domains_get_url_forwards")

        result = await tool_fn(mock_context, domain="example.com")

        assert len(result) == 1
        assert isinstance(result[0], URLForward)
        assert result[0].location == "https://example.org"


class TestDomainsAddUrlForward:
    """Tests for domains_add_url_forward tool."""

    async def test_add_url_forward_success(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_add_url_forward should create a forwarding rule."""
        mcp = _register_domains()
        tool_fn = get_tool_fn(mcp, "domains_add_url_forward")

        result = await tool_fn(
            mock_context,
            domain="example.com",
            location="https://example.org",
            subdomain="www",
        )

        assert isinstance(result, URLForwardCreated)
        assert result.status == "created"
        mock_piglet.domains.add_url_forward.assert_called_once()


class TestDomainsDeleteUrlForward:
    """Tests for domains_delete_url_forward tool."""

    async def test_delete_url_forward_success(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_delete_url_forward should delete a forwarding rule."""
        mcp = _register_domains()
        tool_fn = get_tool_fn(mcp, "domains_delete_url_forward")

        result = await tool_fn(mock_context, domain="example.com", forward_id="123")

        assert isinstance(result, URLForwardCreated)
        assert result.status == "deleted"
        mock_piglet.domains.delete_url_forward.assert_called_once()


class TestDomainsGetGlueRecords:
    """Tests for domains_get_glue_records tool."""

    async def test_get_glue_records_returns_list(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_get_glue_records should return list of GlueRecord."""
        mock_glue = MagicMock()
        mock_glue.hostname = "ns1.example.com"
        mock_glue.ipv4 = ["192.0.2.1"]
        mock_glue.ipv6 = ["2001:db8::1"]
        mock_piglet.domains.get_glue_records.return_value = [mock_glue]
        mcp = _register_domains()
        tool_fn = get_tool_fn(mcp, "domains_get_glue_records")

        result = await tool_fn(mock_context, domain="example.com")

        assert len(result) == 1
        assert isinstance(result[0], GlueRecord)
        assert result[0].hostname == "ns1.example.com"


class TestDomainsCreateGlueRecord:
    """Tests for domains_create_glue_record tool."""

    async def test_create_glue_record_success(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_create_glue_record should create a glue record."""
        mcp = _register_domains()
        tool_fn = get_tool_fn(mcp, "domains_create_glue_record")

        result = await tool_fn(
            mock_context,
            domain="example.com",
            subdomain="ns1",
            ips=["192.0.2.1", "2001:db8::1"],
        )

        assert isinstance(result, GlueRecordCreated)
        assert result.status == "created"
        mock_piglet.domains.create_glue_record.assert_called_once()


class TestDomainsUpdateGlueRecord:
    """Tests for domains_update_glue_record tool."""

    async def test_update_glue_record_success(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_update_glue_record should update a glue record."""
        mcp = _register_domains()
        tool_fn = get_tool_fn(mcp, "domains_update_glue_record")

        result = await tool_fn(
            mock_context,
            domain="example.com",
            subdomain="ns1",
            ips=["192.0.2.2"],
        )

        assert isinstance(result, GlueRecordCreated)
        assert result.status == "updated"
        mock_piglet.domains.update_glue_record.assert_called_once()


class TestDomainsDeleteGlueRecord:
    """Tests for domains_delete_glue_record tool."""

    async def test_delete_glue_record_success(
        self, mock_context: MagicMock, mock_piglet: AsyncMock
    ) -> None:
        """domains_delete_glue_record should delete a glue record."""
        mcp = _register_domains()
        tool_fn = get_tool_fn(mcp, "domains_delete_glue_record")

        result = await tool_fn(mock_context, domain="example.com", subdomain="ns1")

        assert isinstance(result, GlueRecordCreated)
        assert result.status == "deleted"
        mock_piglet.domains.delete_glue_record.assert_called_once()

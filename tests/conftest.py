"""Shared pytest fixtures for porkbun-mcp tests."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastmcp import Context, FastMCP

from porkbun_mcp.server import AppContext


def get_tool_fn(mcp: FastMCP, name: str) -> Callable[..., Coroutine[Any, Any, Any]]:
    """Get a tool function from FastMCP by name."""
    return mcp._tool_manager._tools[name].fn  # type: ignore[attr-defined,return-value]


@pytest.fixture
def mock_piglet() -> AsyncMock:
    """Mock AsyncPiglet client."""
    piglet = AsyncMock()

    # DNS API
    piglet.dns = AsyncMock()
    piglet.dns.list = AsyncMock(return_value=[])
    piglet.dns.get = AsyncMock(return_value=None)
    piglet.dns.get_by_name_type = AsyncMock(return_value=[])
    piglet.dns.create = AsyncMock(return_value="12345")
    piglet.dns.edit = AsyncMock(return_value=None)
    piglet.dns.delete = AsyncMock(return_value=None)
    piglet.dns.delete_by_name_type = AsyncMock(return_value=None)

    # DNSSEC API
    piglet.dnssec = AsyncMock()
    piglet.dnssec.list = AsyncMock(return_value=[])
    piglet.dnssec.create = AsyncMock(return_value=None)
    piglet.dnssec.delete = AsyncMock(return_value=None)

    # Domains API
    piglet.domains = AsyncMock()
    piglet.domains.list = AsyncMock(return_value=[])
    piglet.domains.get_nameservers = AsyncMock(return_value=[])
    piglet.domains.update_nameservers = AsyncMock(return_value=None)
    piglet.domains.get_url_forwards = AsyncMock(return_value=[])
    piglet.domains.add_url_forward = AsyncMock(return_value=None)
    piglet.domains.delete_url_forward = AsyncMock(return_value=None)
    piglet.domains.check = AsyncMock()
    piglet.domains.get_glue_records = AsyncMock(return_value=[])
    piglet.domains.create_glue_record = AsyncMock(return_value=None)
    piglet.domains.update_glue_record = AsyncMock(return_value=None)
    piglet.domains.delete_glue_record = AsyncMock(return_value=None)
    piglet.dns.edit_by_name_type = AsyncMock(return_value=None)

    # SSL API
    piglet.ssl = AsyncMock()
    piglet.ssl.retrieve = AsyncMock()

    # Ping
    piglet.ping = AsyncMock()

    return piglet


@pytest.fixture
def mock_lifespan_context(mock_piglet: AsyncMock) -> AppContext:
    """Mock lifespan context with typed AppContext."""
    return AppContext(piglet=mock_piglet)


@pytest.fixture
def mock_context(mock_lifespan_context: AppContext) -> MagicMock:
    """Mock FastMCP Context."""
    ctx = MagicMock(spec=Context)
    ctx.request_context = MagicMock()
    ctx.request_context.lifespan_context = mock_lifespan_context
    return ctx


def make_mock_dns_record(
    id: str = "12345",
    record_type: str = "A",
    name: str = "www.example.com",
    content: str = "192.0.2.1",
    ttl: int = 600,
    priority: int | None = None,
    notes: str | None = None,
) -> MagicMock:
    """Create a mock DNS record with all fields."""
    record = MagicMock()
    record.id = id
    record.record_type = record_type
    record.name = name
    record.content = content
    record.ttl = ttl
    record.priority = priority
    record.notes = notes
    return record


def make_mock_domain(
    domain: str = "example.com",
    status: str = "ACTIVE",
    tld: str = "com",
    create_date: Any = None,
    expire_date: Any = None,
    security_lock: bool = True,
    whois_privacy: bool = True,
    auto_renew: bool = True,
) -> MagicMock:
    """Create a mock domain with all fields."""
    mock = MagicMock()
    mock.domain = domain
    mock.status = status
    mock.tld = tld
    mock.create_date = create_date
    mock.expire_date = expire_date
    mock.security_lock = security_lock
    mock.whois_privacy = whois_privacy
    mock.auto_renew = auto_renew
    return mock

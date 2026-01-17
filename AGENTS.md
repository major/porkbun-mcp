# porkbun-mcp - Agent Guidelines

MCP server for Porkbun DNS API. Python 3.14+, FastMCP 2.14+, async-first via oinker.

## Quick Reference

```bash
# Install dependencies
uv sync --dev

# Run all checks (lint, format, typecheck, test)
make check

# Individual commands
make lint          # ruff check .
make format        # ruff format .
make typecheck     # ty check
make test          # pytest with coverage

# Run single test file
uv run pytest tests/test_dns_tools.py

# Run single test by name
uv run pytest -k "test_dns_list"

# Fix lint issues automatically
make fix

# Run the MCP server
uv run porkbun-mcp                    # Read-only mode
uv run porkbun-mcp --get-muddy        # Write operations enabled
uv run porkbun-mcp --transport sse    # SSE transport
```

## Project Structure

```
src/porkbun_mcp/
├── __init__.py           # Public API + main() entry point
├── server.py             # FastMCP server setup + lifespan
├── config.py             # PorkbunMCPSettings (pydantic-settings)
├── models.py             # Pydantic response models (output schemas)
├── errors.py             # Oinker -> MCP error mapping
├── tools/
│   ├── __init__.py       # register_tools()
│   ├── ping.py           # ping tool
│   ├── dns.py            # DNS record tools (list, get, create, edit, delete)
│   ├── domains.py        # Domain management tools
│   ├── dnssec.py         # DNSSEC tools
│   ├── ssl.py            # SSL certificate tools
│   └── pricing.py        # TLD pricing tool
└── resources/
    ├── __init__.py       # register_resources()
    ├── domains.py        # porkbun://domains
    ├── dns.py            # porkbun://dns/{domain}
    ├── ssl.py            # porkbun://ssl/{domain}
    └── pricing.py        # porkbun://pricing
```

## Code Style

### General Principles

- **Async-first**: All tools and resources are async functions
- **Pydantic models**: Response models for strict output schemas
- **Type hints everywhere**: Full type annotations with `Annotated[type, Field(...)]`
- **Single-purpose functions**: Small, focused, testable

### Imports

```python
from __future__ import annotations  # Always first

from typing import TYPE_CHECKING, Annotated

from fastmcp import Context, FastMCP
from fastmcp.exceptions import ToolError
from pydantic import BaseModel, Field

from porkbun_mcp.config import PorkbunMCPSettings
from porkbun_mcp.errors import handle_oinker_error
from porkbun_mcp.models import DNSRecord

if TYPE_CHECKING:
    from oinker import AsyncPiglet
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Response models | PascalCase | `DNSRecord`, `PingResult` |
| Tool functions | snake_case | `dns_list()`, `dns_create()` |
| Constants | SCREAMING_SNAKE | `DEFAULT_TTL` |
| Private | Leading underscore | `_validate_domain()` |

### Tool Definitions

```python
from typing import Annotated
from fastmcp import Context
from pydantic import Field

from porkbun_mcp.models import DNSRecord
from porkbun_mcp.errors import handle_oinker_error


async def dns_list(
    ctx: Context,
    domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
) -> list[DNSRecord]:
    """List all DNS records for a domain.

    Returns all DNS records including A, AAAA, MX, TXT, CNAME, and other types.
    """
    piglet = ctx.request_context.lifespan_context["piglet"]

    try:
        records = await piglet.dns.list(domain)
        return [
            DNSRecord(
                id=r.id,
                type=r.record_type,
                name=r.name,
                content=r.content,
                ttl=r.ttl,
                priority=r.priority,
                notes=r.notes,
            )
            for r in records
        ]
    except Exception as e:
        raise handle_oinker_error(e, f"list DNS records for {domain}") from e
```

### Write Tool Guard Pattern

```python
async def dns_create(
    ctx: Context,
    domain: Annotated[str, Field(description="Domain name")],
    record_type: Annotated[str, Field(description="DNS record type")],
    content: Annotated[str, Field(description="Record content")],
) -> DNSRecordCreated:
    """Create a new DNS record. Requires --get-muddy mode."""
    settings: PorkbunMCPSettings = ctx.request_context.lifespan_context["settings"]

    if not settings.get_muddy:
        raise ToolError(
            "Write operations require --get-muddy mode. "
            "Restart with PORKBUN_GET_MUDDY=true or --get-muddy flag."
        )

    # ... implementation
```

### Error Handling

```python
from fastmcp.exceptions import ToolError
from oinker import (
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    APIError,
)


def handle_oinker_error(e: Exception, operation: str) -> ToolError:
    """Convert oinker exceptions to MCP ToolErrors."""
    match e:
        case AuthenticationError():
            return ToolError("Authentication failed. Check credentials.")
        case NotFoundError():
            return ToolError(f"Not found: {e}")
        case RateLimitError() as rle:
            msg = f"Rate limited. Retry in {rle.retry_after}s." if rle.retry_after else "Rate limited."
            return ToolError(msg)
        case _:
            return ToolError(f"Error during {operation}: {e}")
```

### Docstrings (PEP 257 Google style)

**All public functions require docstrings.** Enforced via `make lint`.

```python
async def dns_create(
    ctx: Context,
    domain: Annotated[str, Field(description="Domain name")],
    record_type: Annotated[str, Field(description="DNS record type")],
    content: Annotated[str, Field(description="Record content")],
    ttl: Annotated[int, Field(ge=600, description="TTL in seconds")] = 600,
) -> DNSRecordCreated:
    """Create a new DNS record for a domain.

    Requires --get-muddy mode to be enabled.

    Args:
        ctx: MCP context with piglet client.
        domain: The domain name (e.g., "example.com").
        record_type: DNS record type (A, AAAA, MX, TXT, etc.).
        content: Record content (IP address, hostname, text, etc.).
        ttl: Time to live in seconds (minimum 600).

    Returns:
        DNSRecordCreated with the new record's ID.

    Raises:
        ToolError: If not in --get-muddy mode or API call fails.
    """
```

## Testing Patterns

### Async Tests

pytest-asyncio with `asyncio_mode = "auto"` - no decorators needed:

```python
class TestDNSTools:
    async def test_dns_list_returns_records(self, mock_context: Context) -> None:
        """dns_list should return list of DNSRecord models."""
        result = await dns_list(mock_context, "example.com")

        assert isinstance(result, list)
        assert all(isinstance(r, DNSRecord) for r in result)
```

### Testing Write Guard

```python
async def test_dns_create_blocked_without_get_muddy(
    self, mock_context_readonly: Context
) -> None:
    """dns_create should raise ToolError without --get-muddy."""
    with pytest.raises(ToolError, match="--get-muddy"):
        await dns_create(mock_context_readonly, "example.com", "A", "1.2.3.4")
```

### Fixtures (conftest.py)

```python
import pytest
from unittest.mock import AsyncMock

from porkbun_mcp.config import PorkbunMCPSettings


@pytest.fixture
def mock_settings() -> PorkbunMCPSettings:
    return PorkbunMCPSettings(
        api_key="test_key",
        secret_key="test_secret",
        get_muddy=False,
    )


@pytest.fixture
def mock_piglet() -> AsyncMock:
    piglet = AsyncMock()
    # Configure mock responses
    return piglet
```

## Key Design Patterns

1. **Lifespan for client management**: `AsyncPiglet` created in lifespan, accessed via context
2. **Read-only by default**: `--get-muddy` flag required for write operations
3. **Pydantic response models**: Strict output schemas for all tools
4. **oinker's create_record()**: Factory function for DNS record creation
5. **Error mapping**: All oinker exceptions converted to `ToolError`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORKBUN_API_KEY` | Porkbun API key | (required) |
| `PORKBUN_SECRET_KEY` | Porkbun secret key | (required) |
| `PORKBUN_GET_MUDDY` | Enable write operations | `false` |

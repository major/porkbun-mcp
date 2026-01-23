# porkbun-mcp

MCP server for the [Porkbun](https://porkbun.com/) DNS API.

Manage DNS records, domains, DNSSEC, SSL certificates, and more via the Model Context Protocol.

[![CI](https://github.com/major/porkbun-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/major/porkbun-mcp/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/major/porkbun-mcp/branch/main/graph/badge.svg)](https://codecov.io/gh/major/porkbun-mcp)
[![PyPI version](https://badge.fury.io/py/porkbun-mcp.svg)](https://pypi.org/project/porkbun-mcp/)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Configuration

Set your Porkbun API credentials as environment variables:

```bash
export PORKBUN_API_KEY="pk1_..."
export PORKBUN_SECRET_KEY="sk1_..."
```

Get your API keys from the [Porkbun API Access page](https://porkbun.com/account/api).

## Read-Only Mode (Default)

By default, porkbun-mcp runs in **read-only mode** for safety. Write operations
(create, edit, delete) will return an error until explicitly enabled.

### Enabling Write Operations

To let the pig get muddy and make changes:

**Environment variable:**

```bash
export PORKBUN_GET_MUDDY=true
```

**CLI flag:**

```bash
uvx porkbun-mcp --get-muddy
```

## Usage

Run directly with [uvx](https://docs.astral.sh/uv/) (no installation required):

```bash
uvx porkbun-mcp
```

### SSE transport

```bash
uvx porkbun-mcp --transport sse
```

## MCP Client Configuration

### Claude Desktop

Add to `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "porkbun": {
      "command": "uvx",
      "args": ["porkbun-mcp", "--get-muddy"],
      "env": {
        "PORKBUN_API_KEY": "pk1_...",
        "PORKBUN_SECRET_KEY": "sk1_..."
      }
    }
  }
}
```

> **Note:** Remove `--get-muddy` from args for read-only mode (recommended for safety).

### Claude Code / Codex

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "porkbun": {
      "command": "uvx",
      "args": ["porkbun-mcp", "--get-muddy"],
      "env": {
        "PORKBUN_API_KEY": "pk1_...",
        "PORKBUN_SECRET_KEY": "sk1_..."
      }
    }
  }
}
```

### VS Code

Add to `.vscode/mcp.json` in your workspace (or use `MCP: Add Server` command):

```json
{
  "servers": {
    "porkbun": {
      "command": "uvx",
      "args": ["porkbun-mcp", "--get-muddy"],
      "env": {
        "PORKBUN_API_KEY": "pk1_...",
        "PORKBUN_SECRET_KEY": "sk1_..."
      }
    }
  }
}
```

### OpenCode

Add to your `opencode.json` configuration:

```json
{
  "mcp": {
    "porkbun": {
      "type": "local",
      "command": ["uvx", "porkbun-mcp", "--get-muddy"],
      "environment": {
        "PORKBUN_API_KEY": "pk1_...",
        "PORKBUN_SECRET_KEY": "sk1_..."
      }
    }
  }
}
```

## Available Tools

### DNS

- `dns_list` - List all DNS records for a domain
- `dns_get` - Get a specific DNS record by ID
- `dns_get_by_name_type` - Get DNS records by subdomain and type
- `dns_create` - Create a new DNS record
- `dns_edit` - Edit a DNS record by ID
- `dns_edit_by_name_type` - Edit DNS records by subdomain and type
- `dns_delete` - Delete a DNS record by ID
- `dns_delete_by_name_type` - Delete DNS records by subdomain and type

### Domains

- `domains_list` - List all domains in your account
- `domains_get_nameservers` - Get nameservers for a domain
- `domains_update_nameservers` - Update nameservers for a domain
- `domains_get_url_forwards` - Get URL forwarding rules
- `domains_add_url_forward` - Add a URL forwarding rule
- `domains_delete_url_forward` - Delete a URL forwarding rule
- `domains_check_availability` - Check domain availability and pricing
- `domains_get_glue_records` - Get glue records for a domain

### DNSSEC

- `dnssec_list` - List DNSSEC records for a domain
- `dnssec_create` - Create a DNSSEC record
- `dnssec_delete` - Delete a DNSSEC record

### SSL

- `ssl_retrieve` - Retrieve the SSL certificate bundle for a domain

### Pricing

- `pricing_get` - Get pricing for all available TLDs

### Utility

- `ping` - Test API connectivity and get your public IP

## Prompts

Pre-defined workflows to guide common DNS operations:

- `dns_setup` - Set up basic DNS for a new server (root A + www records)
- `dns_audit` - Audit DNS configuration for issues (duplicates, missing email records, low TTLs)
- `email_dns_setup` - Configure email DNS (MX, SPF, DKIM, DMARC)
- `update_server_ip` - Update DNS records when migrating to a new server IP
- `subdomain_setup` - Create A/CNAME records for a new subdomain

## Development

```bash
# Install dependencies
uv sync --dev

# Run all checks
make check

# Individual commands
make lint       # ruff check
make format     # ruff format
make typecheck  # ty check
make test       # pytest with coverage
```

## License

MIT

<!-- mcp-name: io.github.major/porkbun -->

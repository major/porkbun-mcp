# porkbun-mcp

MCP server for the [Porkbun](https://porkbun.com/) DNS API.

Manage DNS records, domains, DNSSEC, SSL certificates, and more via the Model Context Protocol.

## Installation

```bash
pip install porkbun-mcp
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add porkbun-mcp
```

## Configuration

Set your Porkbun API credentials as environment variables:

```bash
export PORKBUN_API_KEY="pk1_..."
export PORKBUN_SECRET_KEY="sk1_..."
```

Get your API keys from the [Porkbun API Access page](https://porkbun.com/account/api).

## Usage

### Read-only mode (default)

```bash
porkbun-mcp
```

### Enable write operations

```bash
porkbun-mcp --get-muddy
```

Or set `PORKBUN_GET_MUDDY=true` in your environment.

### SSE transport

```bash
porkbun-mcp --transport sse
```

## MCP Client Configuration

### Claude Desktop

Add to `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "porkbun": {
      "command": "porkbun-mcp",
      "env": {
        "PORKBUN_API_KEY": "pk1_...",
        "PORKBUN_SECRET_KEY": "sk1_..."
      }
    }
  }
}
```

For write operations, add `"args": ["--get-muddy"]`.

## Available Tools

### DNS

- `dns_list` - List all DNS records for a domain
- `dns_get` - Get a specific DNS record by ID
- `dns_get_by_name_type` - Get DNS records by subdomain and type
- `dns_create` - Create a new DNS record *
- `dns_edit` - Edit a DNS record by ID *
- `dns_delete` - Delete a DNS record by ID *
- `dns_delete_by_name_type` - Delete DNS records by subdomain and type *

### Domains

- `domains_list` - List all domains in your account
- `domains_get_nameservers` - Get nameservers for a domain
- `domains_update_nameservers` - Update nameservers for a domain *
- `domains_get_url_forwards` - Get URL forwarding rules
- `domains_add_url_forward` - Add a URL forwarding rule *
- `domains_delete_url_forward` - Delete a URL forwarding rule *
- `domains_check_availability` - Check domain availability and pricing
- `domains_get_glue_records` - Get glue records for a domain

### DNSSEC

- `dnssec_list` - List DNSSEC records for a domain
- `dnssec_create` - Create a DNSSEC record *
- `dnssec_delete` - Delete a DNSSEC record *

### SSL

- `ssl_retrieve` - Retrieve the SSL certificate bundle for a domain

### Pricing

- `pricing_get` - Get pricing for all available TLDs

### Utility

- `ping` - Test API connectivity and get your public IP

\* Requires `--get-muddy` mode

## Resources

Browse data via MCP resources:

- `porkbun://domains` - List all domains
- `porkbun://dns/{domain}` - DNS records for a domain
- `porkbun://ssl/{domain}` - SSL certificate bundle for a domain
- `porkbun://pricing` - TLD pricing information

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

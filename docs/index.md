# porkbun-mcp

MCP server for the [Porkbun](https://porkbun.com/) DNS API.

Manage DNS records, domains, DNSSEC, SSL certificates, and more via the Model Context Protocol.

## Features

- **Full DNS management** - Create, edit, delete DNS records
- **Domain tools** - Nameservers, URL forwarding, glue records
- **DNSSEC support** - Manage DNSSEC records
- **SSL certificates** - Retrieve SSL bundles for domains
- **MCP Resources** - Browse data via `porkbun://` URIs
- **Safe by default** - Read-only mode prevents accidental changes

## Quick Start

```bash
pip install porkbun-mcp
```

Set your credentials:

```bash
export PORKBUN_API_KEY="pk1_..."
export PORKBUN_SECRET_KEY="sk1_..."
```

Run the server:

```bash
porkbun-mcp
```

## Requirements

- Python 3.14+
- Porkbun API credentials ([get them here](https://porkbun.com/account/api))

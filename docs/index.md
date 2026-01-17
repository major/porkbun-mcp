# porkbun-mcp

MCP server for the [Porkbun](https://porkbun.com/) DNS API.

Manage DNS records, domains, DNSSEC, SSL certificates, and more via the Model Context Protocol.

## Features

- **Read-only by default** - Write operations require `--get-muddy` flag
- **Full DNS management** - Create, edit, delete DNS records
- **Domain tools** - Nameservers, URL forwarding, glue records
- **DNSSEC support** - Manage DNSSEC records
- **SSL certificates** - Retrieve SSL bundles for domains
- **MCP Resources** - Browse data via `porkbun://` URIs

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
porkbun-mcp              # Read-only mode
porkbun-mcp --get-muddy  # Enable write operations
```

## Why "Get Muddy"?

Porkbun's mascot is a pig. Pigs love mud. When you enable write operations, you're ready to get your hands dirty and make changes to your DNS records.

## Requirements

- Python 3.14+
- Porkbun API credentials ([get them here](https://porkbun.com/account/api))

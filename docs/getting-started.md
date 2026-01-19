# Getting Started

## Installation

Install from PyPI:

```bash
pip install porkbun-mcp
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add porkbun-mcp
```

## Configuration

### API Credentials

Get your API keys from the [Porkbun API Access page](https://porkbun.com/account/api).

Set them as environment variables:

```bash
export PORKBUN_API_KEY="pk1_..."
export PORKBUN_SECRET_KEY="sk1_..."
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

### Other MCP Clients

porkbun-mcp supports both stdio (default) and SSE transports:

```bash
# stdio (default)
porkbun-mcp

# SSE transport
porkbun-mcp --transport sse
```

## Verify Setup

Test your connection with the `ping` tool. It will return your public IP address if credentials are valid.

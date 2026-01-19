# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it privately:

1. **Email**: major@mhtx.net
2. **Subject**: `[SECURITY] porkbun-mcp: <brief description>`

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes (optional)

## Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 7 days
- **Fix timeline**: Depends on severity, typically within 30 days

## Security Considerations

### API Credentials

porkbun-mcp uses Porkbun API credentials for authentication. Credentials are:
- Loaded from environment variables (`PORKBUN_API_KEY`, `PORKBUN_SECRET_KEY`)
- Never logged or exposed in error messages
- Transmitted securely via HTTPS to Porkbun API

### Write Operations

By default, porkbun-mcp allows all DNS operations. For production use, consider:
- Using read-only API keys when possible
- Implementing network-level access controls
- Monitoring DNS changes through Porkbun's dashboard

### Recommendations

1. **API keys**: Use environment variables, never command-line arguments
2. **Key rotation**: Rotate API keys periodically
3. **Least privilege**: Use separate API keys for different environments

"""DNS-related prompt templates for guiding LLM workflows."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from pydantic import Field

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_dns_prompts(mcp: "FastMCP") -> None:
    """Register DNS prompt templates with the MCP server."""

    @mcp.prompt
    def dns_setup(
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        server_ip: Annotated[str, Field(description="IP address of the server")],
    ) -> str:
        """Set up basic DNS records for a new server (root A + www)."""
        return f"""Set up DNS records for {domain} pointing to {server_ip}:

1. First, use dns_list to check existing DNS records
2. Create/update the root A record to point to {server_ip}
3. Create/update the www subdomain (A record or CNAME to root)
4. Verify changes with dns_get_by_name_type

Domain: {domain}
Server IP: {server_ip}
"""

    @mcp.prompt
    def dns_audit(
        domain: Annotated[str, Field(description="Domain name to audit")],
    ) -> str:
        """Audit DNS configuration for potential issues."""
        return f"""Audit DNS configuration for {domain}:

1. List all DNS records with dns_list
2. Check for common issues:
   - Duplicate A/AAAA records for the same subdomain
   - CNAMEs pointing to non-existent targets
   - Missing email records (MX, SPF, DKIM, DMARC)
   - Unusually low TTL values (below 300)
   - Orphaned records for removed services
3. Summarize findings and suggest improvements

Domain: {domain}
"""

    @mcp.prompt
    def email_dns_setup(
        domain: Annotated[str, Field(description="Domain name for email")],
        provider: Annotated[
            str, Field(description="Email provider (e.g., 'google', 'microsoft', 'generic')")
        ] = "generic",
    ) -> str:
        """Set up DNS records for email delivery (MX, SPF, DKIM, DMARC)."""
        return f"""Configure email DNS records for {domain} with provider: {provider}

1. First, check existing MX and TXT records with dns_list
2. Set up or verify MX records for mail routing
3. Add SPF record (TXT at root): defines authorized mail servers
4. Add DKIM record (TXT at selector._domainkey): email signing
5. Add DMARC record (TXT at _dmarc): policy for failed auth

Common patterns:
- SPF: "v=spf1 include:_spf.google.com ~all" (for Google)
- DMARC: "v=DMARC1; p=quarantine; rua=mailto:dmarc@{domain}"

Domain: {domain}
Provider: {provider}

Note: Get exact records from your email provider's documentation.
"""

    @mcp.prompt
    def update_server_ip(
        old_ip: Annotated[str, Field(description="Current/old IP address")],
        new_ip: Annotated[str, Field(description="New IP address")],
    ) -> str:
        """Update DNS records when migrating to a new server IP."""
        return f"""Update DNS records from {old_ip} to {new_ip}:

1. List all domains with domains_list
2. For each domain:
   a. Get all DNS records with dns_list
   b. Find A records with content matching "{old_ip}"
   c. Update each matching record with dns_edit or dns_edit_by_name_type
3. Verify all changes

Old IP: {old_ip}
New IP: {new_ip}

Tip: Lower TTL before migration, then raise it after.
"""

    @mcp.prompt
    def subdomain_setup(
        domain: Annotated[str, Field(description="Root domain name")],
        subdomain: Annotated[str, Field(description="Subdomain to create (e.g., 'api', 'blog')")],
        target: Annotated[str, Field(description="Target IP or hostname for the subdomain")],
    ) -> str:
        """Set up a new subdomain pointing to a target."""
        return f"""Set up subdomain {subdomain}.{domain} pointing to {target}:

1. Check if {subdomain} already exists with dns_get_by_name_type
2. Determine record type:
   - If target is an IP address: create A record
   - If target is a hostname: create CNAME record
3. Create the record with dns_create
4. Verify with dns_get_by_name_type

Subdomain: {subdomain}.{domain}
Target: {target}
"""

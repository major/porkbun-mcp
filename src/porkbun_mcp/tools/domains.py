"""Domain management tools for the Porkbun MCP server."""

from typing import TYPE_CHECKING, Annotated

from fastmcp import Context
from fastmcp.exceptions import ToolError
from pydantic import Field

from porkbun_mcp.context import get_piglet, require_writes
from porkbun_mcp.errors import handle_oinker_error
from porkbun_mcp.models import (
    DomainAvailability,
    DomainInfo,
    GlueRecord,
    GlueRecordCreated,
    Nameservers,
    URLForward,
    URLForwardCreated,
)

if TYPE_CHECKING:
    from fastmcp import FastMCP

from typing import Any


def _to_domain_info(d: Any) -> DomainInfo:
    """Convert oinker domain to Pydantic model."""
    return DomainInfo(
        domain=d.domain,
        status=d.status,
        tld=d.tld,
        create_date=d.create_date.isoformat() if d.create_date else None,
        expire_date=d.expire_date.isoformat() if d.expire_date else None,
        security_lock=d.security_lock,
        whois_privacy=d.whois_privacy,
        auto_renew=d.auto_renew,
    )


def register_domain_tools(mcp: "FastMCP") -> None:
    """Register domain tools with the MCP server."""

    @mcp.tool(annotations={"readOnlyHint": True})
    async def domains_list(ctx: Context) -> list[DomainInfo]:
        """List all domains in your Porkbun account."""
        piglet = get_piglet(ctx)

        try:
            domains = await piglet.domains.list()
            return [_to_domain_info(d) for d in domains]
        except Exception as e:
            raise handle_oinker_error(e, "list domains") from e

    @mcp.tool(annotations={"readOnlyHint": True})
    async def domains_get_nameservers(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
    ) -> Nameservers:
        """Get nameservers for a domain."""
        piglet = get_piglet(ctx)

        try:
            ns = await piglet.domains.get_nameservers(domain)
            return Nameservers(domain=domain, nameservers=list(ns))
        except Exception as e:
            raise handle_oinker_error(e, f"get nameservers for {domain}") from e

    @mcp.tool(annotations={"idempotentHint": True})
    async def domains_update_nameservers(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        nameservers: Annotated[list[str], Field(description="List of nameservers")],
    ) -> Nameservers:
        """Update nameservers for a domain."""
        require_writes(ctx)
        piglet = get_piglet(ctx)

        try:
            await piglet.domains.update_nameservers(domain, nameservers)
            return Nameservers(domain=domain, nameservers=nameservers)
        except Exception as e:
            raise handle_oinker_error(e, f"update nameservers for {domain}") from e

    @mcp.tool(annotations={"readOnlyHint": True})
    async def domains_get_url_forwards(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
    ) -> list[URLForward]:
        """Get URL forwarding rules for a domain."""
        piglet = get_piglet(ctx)

        try:
            forwards = await piglet.domains.get_url_forwards(domain)
            return [
                URLForward(
                    id=f.id,
                    subdomain=f.subdomain,
                    location=f.location,
                    type=f.type,
                    include_path=f.include_path,
                    wildcard=f.wildcard,
                )
                for f in forwards
            ]
        except Exception as e:
            raise handle_oinker_error(e, f"get URL forwards for {domain}") from e

    @mcp.tool(annotations={"idempotentHint": False})
    async def domains_add_url_forward(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        location: Annotated[str, Field(description="Destination URL")],
        subdomain: Annotated[str | None, Field(description="Subdomain (None for root)")] = None,
        forward_type: Annotated[
            str, Field(description="Redirect type: 'temporary' or 'permanent'")
        ] = "temporary",
        include_path: Annotated[bool, Field(description="Include URI path in redirect")] = False,
        wildcard: Annotated[bool, Field(description="Forward all subdomains")] = False,
    ) -> URLForwardCreated:
        """Add a URL forwarding rule."""
        require_writes(ctx)
        piglet = get_piglet(ctx)

        try:
            from oinker.domains import URLForwardCreate

            forward = URLForwardCreate(
                location=location,
                type=forward_type,  # type: ignore[arg-type]
                subdomain=subdomain,
                include_path=include_path,
                wildcard=wildcard,
            )
            await piglet.domains.add_url_forward(domain, forward)
            return URLForwardCreated(status="created", message=f"URL forward created for {domain}")
        except ToolError:
            raise
        except Exception as e:
            raise handle_oinker_error(e, f"add URL forward for {domain}") from e

    @mcp.tool(annotations={"destructiveHint": True})
    async def domains_delete_url_forward(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        forward_id: Annotated[str, Field(description="URL forward ID to delete")],
    ) -> URLForwardCreated:
        """Delete a URL forwarding rule."""
        require_writes(ctx)
        piglet = get_piglet(ctx)

        try:
            await piglet.domains.delete_url_forward(domain, forward_id)
            return URLForwardCreated(status="deleted", message=f"URL forward {forward_id} deleted")
        except Exception as e:
            raise handle_oinker_error(e, f"delete URL forward {forward_id}") from e

    @mcp.tool(annotations={"readOnlyHint": True})
    async def domains_check_availability(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name to check (e.g., 'example.com')")],
    ) -> DomainAvailability:
        """Check domain availability and pricing.

        WARNING: Heavily rate-limited (1 request per 10 seconds).
        For price comparisons, use pricing_get first (no rate limits).
        Only use this tool when you need to confirm a specific domain is available.
        """
        piglet = get_piglet(ctx)

        try:
            result = await piglet.domains.check(domain)
            return DomainAvailability(
                domain=domain,
                available=result.available,
                price=result.price,
                premium=result.premium,
            )
        except Exception as e:
            raise handle_oinker_error(e, f"check availability for {domain}") from e

    @mcp.tool(annotations={"readOnlyHint": True})
    async def domains_get_glue_records(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
    ) -> list[GlueRecord]:
        """Get glue records for a domain."""
        piglet = get_piglet(ctx)

        try:
            glue_records = await piglet.domains.get_glue_records(domain)
            return [
                GlueRecord(
                    hostname=g.hostname,
                    ipv4=list(g.ipv4),
                    ipv6=list(g.ipv6),
                )
                for g in glue_records
            ]
        except Exception as e:
            raise handle_oinker_error(e, f"get glue records for {domain}") from e

    @mcp.tool(annotations={"idempotentHint": False})
    async def domains_create_glue_record(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        subdomain: Annotated[str, Field(description="Subdomain for the nameserver (e.g., 'ns1')")],
        ips: Annotated[list[str], Field(description="List of IP addresses (IPv4 and/or IPv6)")],
    ) -> GlueRecordCreated:
        """Create a glue record for self-hosted nameservers."""
        require_writes(ctx)
        piglet = get_piglet(ctx)

        try:
            await piglet.domains.create_glue_record(domain, subdomain, ips)
            return GlueRecordCreated(
                status="created",
                message=f"Glue record {subdomain}.{domain} created with IPs: {', '.join(ips)}",
            )
        except Exception as e:
            raise handle_oinker_error(e, f"create glue record {subdomain}.{domain}") from e

    @mcp.tool(annotations={"idempotentHint": True})
    async def domains_update_glue_record(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        subdomain: Annotated[str, Field(description="Subdomain for the nameserver (e.g., 'ns1')")],
        ips: Annotated[list[str], Field(description="New list of IP addresses (replaces all)")],
    ) -> GlueRecordCreated:
        """Update a glue record's IP addresses."""
        require_writes(ctx)
        piglet = get_piglet(ctx)

        try:
            await piglet.domains.update_glue_record(domain, subdomain, ips)
            return GlueRecordCreated(
                status="updated",
                message=f"Glue record {subdomain}.{domain} updated with IPs: {', '.join(ips)}",
            )
        except Exception as e:
            raise handle_oinker_error(e, f"update glue record {subdomain}.{domain}") from e

    @mcp.tool(annotations={"destructiveHint": True})
    async def domains_delete_glue_record(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        subdomain: Annotated[str, Field(description="Subdomain of the glue record to delete")],
    ) -> GlueRecordCreated:
        """Delete a glue record."""
        require_writes(ctx)
        piglet = get_piglet(ctx)

        try:
            await piglet.domains.delete_glue_record(domain, subdomain)
            return GlueRecordCreated(
                status="deleted",
                message=f"Glue record {subdomain}.{domain} deleted",
            )
        except Exception as e:
            raise handle_oinker_error(e, f"delete glue record {subdomain}.{domain}") from e

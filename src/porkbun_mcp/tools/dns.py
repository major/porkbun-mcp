"""DNS record tools for the Porkbun MCP server."""

from typing import TYPE_CHECKING, Annotated

from fastmcp import Context
from fastmcp.exceptions import ToolError
from pydantic import Field

from porkbun_mcp.context import get_piglet, require_writes
from porkbun_mcp.errors import handle_oinker_error
from porkbun_mcp.models import DNSRecord, DNSRecordCreated, DNSRecordDeleted

if TYPE_CHECKING:
    from fastmcp import FastMCP

from typing import Any


def _get_dns_record_class(record_type: str) -> type:
    """Get DNS record class for type, or raise ToolError if invalid."""
    from oinker.dns import DNS_RECORD_CLASSES

    record_cls = DNS_RECORD_CLASSES.get(record_type.upper())
    if not record_cls:
        valid_types = ", ".join(sorted(DNS_RECORD_CLASSES.keys()))
        raise ToolError(f"Unknown record type: {record_type}. Valid types: {valid_types}")
    return record_cls


def _to_dns_record(r: Any) -> DNSRecord:
    """Convert oinker DNS record to Pydantic model."""
    return DNSRecord(
        id=r.id,
        type=r.record_type,
        name=r.name,
        content=r.content,
        ttl=r.ttl,
        priority=r.priority,
        notes=r.notes,
    )


def register_dns_tools(mcp: "FastMCP") -> None:
    """Register DNS tools with the MCP server."""

    @mcp.tool(annotations={"readOnlyHint": True})
    async def dns_list(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
    ) -> list[DNSRecord]:
        """List all DNS records for a domain."""
        piglet = get_piglet(ctx)

        try:
            records = await piglet.dns.list(domain)
            return [_to_dns_record(r) for r in records]
        except Exception as e:
            raise handle_oinker_error(e, f"list DNS records for {domain}") from e

    @mcp.tool(annotations={"readOnlyHint": True})
    async def dns_get(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        record_id: Annotated[str, Field(description="DNS record ID")],
    ) -> DNSRecord:
        """Get a specific DNS record by ID."""
        piglet = get_piglet(ctx)

        try:
            r = await piglet.dns.get(domain, record_id)
            if r is None:
                raise ToolError(f"DNS record {record_id} not found for {domain}")
            return _to_dns_record(r)
        except ToolError:
            raise
        except Exception as e:
            raise handle_oinker_error(e, f"get DNS record {record_id}") from e

    @mcp.tool(annotations={"readOnlyHint": True})
    async def dns_get_by_name_type(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        record_type: Annotated[str, Field(description="DNS record type (A, AAAA, MX, etc.)")],
        subdomain: Annotated[
            str | None,
            Field(description="Subdomain (None for root, '*' for wildcard)"),
        ] = None,
    ) -> list[DNSRecord]:
        """Get DNS records by subdomain and type."""
        piglet = get_piglet(ctx)

        try:
            records = await piglet.dns.get_by_name_type(domain, record_type, subdomain)
            return [_to_dns_record(r) for r in records]
        except Exception as e:
            raise handle_oinker_error(
                e, f"get {record_type} records for {subdomain or 'root'}.{domain}"
            ) from e

    @mcp.tool(annotations={"idempotentHint": False})
    async def dns_create(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        record_type: Annotated[
            str,
            Field(description="DNS record type: A, AAAA, MX, TXT, CNAME, ALIAS, NS, SRV, etc."),
        ],
        content: Annotated[str, Field(description="Record content (IP, hostname, text, etc.)")],
        name: Annotated[
            str | None,
            Field(description="Subdomain (None for root, '*' for wildcard)"),
        ] = None,
        ttl: Annotated[int, Field(ge=600, description="TTL in seconds (minimum 600)")] = 600,
        priority: Annotated[
            int | None,
            Field(ge=0, description="Priority for MX/SRV records"),
        ] = None,
    ) -> DNSRecordCreated:
        """Create a new DNS record."""
        require_writes(ctx)
        record_cls = _get_dns_record_class(record_type)
        piglet = get_piglet(ctx)

        try:
            kwargs: dict[str, str | int] = {"content": content, "ttl": ttl}
            if name is not None:
                kwargs["name"] = name
            if priority is not None:
                kwargs["priority"] = priority

            record = record_cls(**kwargs)
            record_id = await piglet.dns.create(domain, record)
            return DNSRecordCreated(status="created", record_id=record_id)
        except Exception as e:
            raise handle_oinker_error(e, f"create {record_type} record for {domain}") from e

    @mcp.tool(annotations={"idempotentHint": True})
    async def dns_edit(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        record_id: Annotated[str, Field(description="DNS record ID to edit")],
        record_type: Annotated[str, Field(description="DNS record type")],
        content: Annotated[str, Field(description="New record content")],
        name: Annotated[str | None, Field(description="New subdomain")] = None,
        ttl: Annotated[int, Field(ge=600, description="New TTL in seconds")] = 600,
        priority: Annotated[int | None, Field(ge=0, description="New priority")] = None,
    ) -> DNSRecordCreated:
        """Edit a DNS record by ID."""
        require_writes(ctx)
        record_cls = _get_dns_record_class(record_type)
        piglet = get_piglet(ctx)

        try:
            kwargs: dict[str, str | int] = {"content": content, "ttl": ttl}
            if name is not None:
                kwargs["name"] = name
            if priority is not None:
                kwargs["priority"] = priority

            record = record_cls(**kwargs)
            await piglet.dns.edit(domain, record_id, record)
            return DNSRecordCreated(status="updated", record_id=record_id)
        except Exception as e:
            raise handle_oinker_error(e, f"edit DNS record {record_id}") from e

    @mcp.tool(annotations={"idempotentHint": True})
    async def dns_edit_by_name_type(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        record_type: Annotated[str, Field(description="DNS record type (A, AAAA, MX, etc.)")],
        content: Annotated[str, Field(description="New record content")],
        subdomain: Annotated[
            str | None,
            Field(description="Subdomain (None for root, '*' for wildcard)"),
        ] = None,
        ttl: Annotated[int | None, Field(ge=600, description="New TTL in seconds")] = None,
        priority: Annotated[int | None, Field(ge=0, description="New priority")] = None,
        notes: Annotated[str | None, Field(description="New notes")] = None,
    ) -> DNSRecordDeleted:
        """Edit all DNS records matching subdomain and type."""
        require_writes(ctx)
        piglet = get_piglet(ctx)

        try:
            await piglet.dns.edit_by_name_type(
                domain,
                record_type,
                subdomain,
                content=content,
                ttl=ttl,
                priority=priority,
                notes=notes,
            )
            name_part = subdomain or "root"
            return DNSRecordDeleted(
                status="updated",
                message=f"Updated {record_type} records for {name_part}.{domain}",
            )
        except Exception as e:
            raise handle_oinker_error(
                e, f"edit {record_type} records for {subdomain or 'root'}.{domain}"
            ) from e

    @mcp.tool(annotations={"destructiveHint": True})
    async def dns_delete(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        record_id: Annotated[str, Field(description="DNS record ID to delete")],
    ) -> DNSRecordDeleted:
        """Delete a DNS record by ID."""
        require_writes(ctx)
        piglet = get_piglet(ctx)

        try:
            await piglet.dns.delete(domain, record_id)
            return DNSRecordDeleted(status="deleted", message=f"Record {record_id} deleted")
        except Exception as e:
            raise handle_oinker_error(e, f"delete DNS record {record_id}") from e

    @mcp.tool(annotations={"destructiveHint": True})
    async def dns_delete_by_name_type(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        record_type: Annotated[str, Field(description="DNS record type")],
        subdomain: Annotated[str | None, Field(description="Subdomain (None for root)")] = None,
    ) -> DNSRecordDeleted:
        """Delete DNS records by subdomain and type."""
        require_writes(ctx)
        piglet = get_piglet(ctx)

        try:
            await piglet.dns.delete_by_name_type(domain, record_type, subdomain)
            name_part = subdomain or "root"
            return DNSRecordDeleted(
                status="deleted", message=f"Deleted {record_type} records for {name_part}.{domain}"
            )
        except Exception as e:
            raise handle_oinker_error(
                e, f"delete {record_type} records for {subdomain or 'root'}.{domain}"
            ) from e

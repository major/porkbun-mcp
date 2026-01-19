"""DNSSEC tools for the Porkbun MCP server."""

from typing import TYPE_CHECKING, Annotated

from fastmcp import Context
from fastmcp.exceptions import ToolError
from pydantic import Field

from porkbun_mcp.context import get_piglet, require_writes
from porkbun_mcp.errors import handle_oinker_error
from porkbun_mcp.models import DNSRecordDeleted, DNSSECRecord

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_dnssec_tools(mcp: "FastMCP") -> None:
    """Register DNSSEC tools with the MCP server."""

    @mcp.tool(annotations={"readOnlyHint": True})
    async def dnssec_list(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
    ) -> list[DNSSECRecord]:
        """List DNSSEC records for a domain."""
        piglet = get_piglet(ctx)

        try:
            records = await piglet.dnssec.list(domain)
            return [
                DNSSECRecord(
                    key_tag=r.key_tag,
                    algorithm=r.algorithm,
                    digest_type=r.digest_type,
                    digest=r.digest,
                )
                for r in records
            ]
        except Exception as e:
            raise handle_oinker_error(e, f"list DNSSEC records for {domain}") from e

    @mcp.tool(annotations={"idempotentHint": False})
    async def dnssec_create(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        key_tag: Annotated[str, Field(description="DNSSEC key tag")],
        algorithm: Annotated[str, Field(description="DS data algorithm")],
        digest_type: Annotated[str, Field(description="Digest type")],
        digest: Annotated[str, Field(description="Digest value")],
    ) -> DNSSECRecord:
        """Create a DNSSEC record."""
        require_writes(ctx)
        piglet = get_piglet(ctx)

        try:
            from oinker.dnssec import DNSSECRecordCreate

            record = DNSSECRecordCreate(
                key_tag=key_tag,
                algorithm=algorithm,
                digest_type=digest_type,
                digest=digest,
            )
            await piglet.dnssec.create(domain, record)
            return DNSSECRecord(
                key_tag=key_tag,
                algorithm=algorithm,
                digest_type=digest_type,
                digest=digest,
            )
        except ToolError:
            raise
        except Exception as e:
            raise handle_oinker_error(e, f"create DNSSEC record for {domain}") from e

    @mcp.tool(annotations={"destructiveHint": True})
    async def dnssec_delete(
        ctx: Context,
        domain: Annotated[str, Field(description="Domain name (e.g., 'example.com')")],
        key_tag: Annotated[str, Field(description="DNSSEC key tag to delete")],
    ) -> DNSRecordDeleted:
        """Delete a DNSSEC record."""
        require_writes(ctx)
        piglet = get_piglet(ctx)

        try:
            await piglet.dnssec.delete(domain, key_tag)
            return DNSRecordDeleted(status="deleted", message=f"DNSSEC record {key_tag} deleted")
        except Exception as e:
            raise handle_oinker_error(e, f"delete DNSSEC record {key_tag}") from e

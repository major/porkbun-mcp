"""Pydantic response models for strict output schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class DNSRecord(BaseModel):
    """A DNS record."""

    id: str = Field(description="Record ID")
    type: str = Field(description="Record type (A, AAAA, MX, etc.)")
    name: str = Field(description="Full record name (e.g., www.example.com)")
    content: str = Field(description="Record content")
    ttl: int = Field(description="Time to live in seconds")
    priority: int | None = Field(default=None, description="Priority (MX, SRV only)")
    notes: str | None = Field(default=None, description="Optional notes")


class OperationResult(BaseModel):
    """Base class for operation results with status and message."""

    status: str = Field(description="Operation status")
    message: str = Field(description="Confirmation message")


class DNSRecordCreated(BaseModel):
    """Result of creating a DNS record."""

    status: str = Field(description="Operation status")
    record_id: str = Field(description="ID of the created record")


class DNSRecordDeleted(OperationResult):
    """Result of deleting a DNS record."""

    pass


class DomainInfo(BaseModel):
    """Information about a domain."""

    domain: str = Field(description="Domain name")
    status: str = Field(description="Domain status (e.g., ACTIVE)")
    tld: str = Field(description="Top-level domain")
    create_date: str | None = Field(default=None, description="Creation date")
    expire_date: str | None = Field(default=None, description="Expiration date")
    security_lock: bool = Field(description="Security lock enabled")
    whois_privacy: bool = Field(description="WHOIS privacy enabled")
    auto_renew: bool = Field(description="Auto-renew enabled")


class Nameservers(BaseModel):
    """Nameservers for a domain."""

    domain: str = Field(description="Domain name")
    nameservers: list[str] = Field(description="List of nameservers")


class URLForward(BaseModel):
    """A URL forwarding rule."""

    id: str = Field(description="Forward rule ID")
    subdomain: str = Field(description="Subdomain (empty for root)")
    location: str = Field(description="Destination URL")
    type: str = Field(description="Redirect type (temporary/permanent)")
    include_path: bool = Field(description="Include URI path")
    wildcard: bool = Field(description="Forward all subdomains")


class URLForwardCreated(OperationResult):
    """Result of URL forward operations."""

    pass


class GlueRecord(BaseModel):
    """A glue record (nameserver with IP addresses)."""

    hostname: str = Field(description="Full hostname")
    ipv4: list[str] = Field(default_factory=list, description="IPv4 addresses")
    ipv6: list[str] = Field(default_factory=list, description="IPv6 addresses")


class GlueRecordCreated(OperationResult):
    """Result of glue record operations."""

    pass


class DomainAvailability(BaseModel):
    """Domain availability check result."""

    domain: str = Field(description="Domain name checked")
    available: bool = Field(description="Whether domain is available")
    price: str = Field(description="Registration price")
    premium: bool = Field(description="Whether this is a premium domain")


class DNSSECRecord(BaseModel):
    """A DNSSEC record."""

    key_tag: str = Field(description="Key tag")
    algorithm: str = Field(description="DS data algorithm")
    digest_type: str = Field(description="Digest type")
    digest: str = Field(description="Digest value")


class SSLBundle(BaseModel):
    """SSL certificate bundle."""

    certificate_chain: str = Field(description="Certificate chain (PEM)")
    private_key: str = Field(description="Private key (PEM)")
    public_key: str = Field(description="Public key (PEM)")


class TLDPricing(BaseModel):
    """Pricing for a TLD."""

    tld: str = Field(description="Top-level domain")
    registration: str = Field(description="Registration price")
    renewal: str = Field(description="Renewal price")
    transfer: str = Field(description="Transfer price")


class PingResult(BaseModel):
    """Result of the ping operation."""

    status: str = Field(description="API status")
    your_ip: str = Field(description="Your public IP address")

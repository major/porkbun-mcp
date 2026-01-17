# Pricing Tools

Tools for retrieving TLD pricing information.

## pricing_get

Get pricing for all available TLDs.

**Returns:** List of TLD pricing with:

- `tld` - Top-level domain (e.g., "com", "net", "org")
- `registration` - Registration price
- `renewal` - Renewal price
- `transfer` - Transfer price

!!! note
    This endpoint does not require authentication.

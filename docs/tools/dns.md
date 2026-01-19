# DNS Tools

Tools for managing DNS records.

## dns_list

List all DNS records for a domain.

**Parameters:**

- `domain` (str): Domain name (e.g., "example.com")

**Returns:** List of DNS records with ID, type, name, content, TTL, priority, and notes.

## dns_get

Get a specific DNS record by ID.

**Parameters:**

- `domain` (str): Domain name
- `record_id` (str): DNS record ID

**Returns:** Single DNS record.

## dns_get_by_name_type

Get DNS records by subdomain and type.

**Parameters:**

- `domain` (str): Domain name
- `record_type` (str): DNS record type (A, AAAA, MX, etc.)
- `subdomain` (str, optional): Subdomain (None for root, "*" for wildcard)

**Returns:** List of matching DNS records.

## dns_create

Create a new DNS record.

**Parameters:**

- `domain` (str): Domain name
- `record_type` (str): DNS record type (A, AAAA, MX, TXT, CNAME, ALIAS, NS, SRV, etc.)
- `content` (str): Record content (IP, hostname, text, etc.)
- `name` (str, optional): Subdomain (None for root, "*" for wildcard)
- `ttl` (int): TTL in seconds (minimum 600, default 600)
- `priority` (int, optional): Priority for MX/SRV records

**Returns:** Created record ID.

## dns_edit

Edit a DNS record by ID.

**Parameters:**

- `domain` (str): Domain name
- `record_id` (str): DNS record ID to edit
- `record_type` (str): DNS record type
- `content` (str): New record content
- `name` (str, optional): New subdomain
- `ttl` (int): New TTL in seconds (minimum 600)
- `priority` (int, optional): New priority

**Returns:** Updated record ID.

## dns_delete

Delete a DNS record by ID.

**Parameters:**

- `domain` (str): Domain name
- `record_id` (str): DNS record ID to delete

**Returns:** Deletion confirmation.

## dns_delete_by_name_type

Delete DNS records by subdomain and type.

**Parameters:**

- `domain` (str): Domain name
- `record_type` (str): DNS record type
- `subdomain` (str, optional): Subdomain (None for root)

**Returns:** Deletion confirmation.

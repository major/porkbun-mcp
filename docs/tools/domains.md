# Domain Tools

Tools for managing domains, nameservers, and URL forwarding.

## domains_list

List all domains in your Porkbun account.

**Returns:** List of domains with status, TLD, creation/expiration dates, and settings.

## domains_get_nameservers

Get nameservers for a domain.

**Parameters:**

- `domain` (str): Domain name

**Returns:** List of nameserver hostnames.

## domains_update_nameservers

Update nameservers for a domain. **Requires `--get-muddy` mode.**

**Parameters:**

- `domain` (str): Domain name
- `nameservers` (list[str]): List of nameservers

**Returns:** Updated nameservers.

## domains_get_url_forwards

Get URL forwarding rules for a domain.

**Parameters:**

- `domain` (str): Domain name

**Returns:** List of URL forwarding rules.

## domains_add_url_forward

Add a URL forwarding rule. **Requires `--get-muddy` mode.**

**Parameters:**

- `domain` (str): Domain name
- `location` (str): Destination URL
- `subdomain` (str, optional): Subdomain (None for root)
- `forward_type` (str): "temporary" or "permanent" (default: "temporary")
- `include_path` (bool): Include URI path in redirect (default: False)
- `wildcard` (bool): Forward all subdomains (default: False)

**Returns:** Creation confirmation.

## domains_delete_url_forward

Delete a URL forwarding rule. **Requires `--get-muddy` mode.**

**Parameters:**

- `domain` (str): Domain name
- `forward_id` (str): URL forward ID to delete

**Returns:** Deletion confirmation.

## domains_check_availability

Check domain availability and pricing.

**Parameters:**

- `domain` (str): Domain name to check

**Returns:** Availability status, price, and premium flag.

## domains_get_glue_records

Get glue records for a domain.

**Parameters:**

- `domain` (str): Domain name

**Returns:** List of glue records with hostname and IP addresses.

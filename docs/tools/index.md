# Tools Overview

porkbun-mcp provides MCP tools for managing your Porkbun domains and DNS records.

## Read-Only Tools

These tools work without `--get-muddy`:

| Tool | Description |
|------|-------------|
| `ping` | Test API connectivity, get your public IP |
| `dns_list` | List all DNS records for a domain |
| `dns_get` | Get a specific DNS record by ID |
| `dns_get_by_name_type` | Get DNS records by subdomain and type |
| `domains_list` | List all domains in your account |
| `domains_get_nameservers` | Get nameservers for a domain |
| `domains_get_url_forwards` | Get URL forwarding rules |
| `domains_check_availability` | Check domain availability and pricing |
| `domains_get_glue_records` | Get glue records for a domain |
| `dnssec_list` | List DNSSEC records for a domain |
| `ssl_retrieve` | Get SSL certificate bundle |
| `pricing_get` | Get pricing for all TLDs |

## Write Tools

These tools require `--get-muddy` mode:

| Tool | Description |
|------|-------------|
| `dns_create` | Create a new DNS record |
| `dns_edit` | Edit a DNS record by ID |
| `dns_delete` | Delete a DNS record by ID |
| `dns_delete_by_name_type` | Delete DNS records by subdomain and type |
| `domains_update_nameservers` | Update nameservers for a domain |
| `domains_add_url_forward` | Add a URL forwarding rule |
| `domains_delete_url_forward` | Delete a URL forwarding rule |
| `dnssec_create` | Create a DNSSEC record |
| `dnssec_delete` | Delete a DNSSEC record |

## MCP Resources

Browse data via MCP resources:

| Resource URI | Description |
|--------------|-------------|
| `porkbun://domains` | List all domains |
| `porkbun://dns/{domain}` | DNS records for a domain |
| `porkbun://ssl/{domain}` | SSL certificate bundle |
| `porkbun://pricing` | TLD pricing information |

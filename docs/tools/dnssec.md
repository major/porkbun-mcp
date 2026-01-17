# DNSSEC Tools

Tools for managing DNSSEC records.

## dnssec_list

List DNSSEC records for a domain.

**Parameters:**

- `domain` (str): Domain name

**Returns:** List of DNSSEC records with key tag, algorithm, digest type, and digest.

## dnssec_create

Create a DNSSEC record. **Requires `--get-muddy` mode.**

**Parameters:**

- `domain` (str): Domain name
- `key_tag` (str): DNSSEC key tag
- `algorithm` (str): DS data algorithm
- `digest_type` (str): Digest type
- `digest` (str): Digest value

**Returns:** Created DNSSEC record.

## dnssec_delete

Delete a DNSSEC record. **Requires `--get-muddy` mode.**

**Parameters:**

- `domain` (str): Domain name
- `key_tag` (str): DNSSEC key tag to delete

**Returns:** Deletion confirmation.

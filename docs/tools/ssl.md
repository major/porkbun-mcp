# SSL Tools

Tools for retrieving SSL certificates.

## ssl_retrieve

Retrieve the SSL certificate bundle for a domain.

Only available for domains using Porkbun nameservers.

**Parameters:**

- `domain` (str): Domain name

**Returns:** SSL bundle containing:

- `certificate_chain` - Certificate chain in PEM format
- `private_key` - Private key in PEM format
- `public_key` - Public key in PEM format

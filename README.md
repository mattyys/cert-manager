# Certificate Manager - Mantenimiento de Certificados

A comprehensive Python tool for managing and tracking SSL/TLS certificate expiration dates.

## Features

- 📋 **Certificate Management**: Add, remove, update, and view certificates
- ⏰ **Expiration Tracking**: Monitor certificate expiration dates
- 🔔 **Alerts**: Identify expired and soon-to-expire certificates
- 📊 **Statistics**: View certificate statistics at a glance
- 💾 **Persistent Storage**: JSON-based storage for certificates
- 🎨 **CLI Interface**: Easy-to-use command-line interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mattyys/cert-manager.git
cd cert-manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Adding a Certificate

Add a new certificate to track:

```bash
python cli.py add mycert example.com 2025-12-31 --issuer "Let's Encrypt" --notes "Production certificate"
```

### Listing Certificates

List all certificates:
```bash
python cli.py list
```

List only expired certificates:
```bash
python cli.py list --expired
```

List certificates expiring soon (within 30 days by default):
```bash
python cli.py list --expiring-soon
```

List certificates expiring in next 7 days:
```bash
python cli.py list --expiring-soon --days 7
```

### Viewing Certificate Details

Show detailed information about a specific certificate:
```bash
python cli.py show mycert
```

### Updating a Certificate

Update certificate information:
```bash
python cli.py update mycert --expiration-date 2026-12-31 --notes "Renewed certificate"
```

### Removing a Certificate

Remove a certificate from tracking:
```bash
python cli.py remove mycert
```

### Viewing Statistics

Display certificate statistics:
```bash
python cli.py stats
```

## Examples

### Example 1: Managing Multiple Certificates

```bash
# Add multiple certificates
python cli.py add web-server example.com 2025-06-30 --issuer "Let's Encrypt"
python cli.py add api-server api.example.com 2025-07-15 --issuer "Let's Encrypt"
python cli.py add mail-server mail.example.com 2025-05-20 --issuer "DigiCert"

# List all certificates
python cli.py list

# Check statistics
python cli.py stats
```

### Example 2: Monitoring Expiring Certificates

```bash
# Check which certificates are expiring in the next 30 days
python cli.py list --expiring-soon

# Check which certificates are expiring in the next 7 days
python cli.py list --expiring-soon --days 7

# Check for expired certificates
python cli.py list --expired
```

### Example 3: Updating a Certificate After Renewal

```bash
# View current certificate details
python cli.py show web-server

# Update with new expiration date after renewal
python cli.py update web-server --expiration-date 2026-06-30 --notes "Certificate renewed"

# Verify the update
python cli.py show web-server
```

## Certificate Storage

Certificates are stored in a JSON file (`certificates.json` by default). You can specify a custom storage location:

```bash
python cli.py --storage /path/to/certificates.json list
```

## Status Indicators

When listing certificates, the following status indicators are shown:

- 🟢 **OK**: Certificate is valid and not expiring soon
- 🟠 **WARNING**: Certificate expires within 30 days
- 🟡 **URGENT**: Certificate expires within 7 days
- 🔴 **EXPIRED**: Certificate has already expired

## Python API

You can also use the Certificate Manager as a Python library:

```python
from cert_manager import Certificate, CertificateManager

# Initialize manager
manager = CertificateManager()

# Add a certificate
cert = Certificate(
    name="mycert",
    domain="example.com",
    expiration_date="2025-12-31",
    issuer="Let's Encrypt",
    notes="Production certificate"
)
manager.add_certificate(cert)

# Get expiring certificates
expiring = manager.get_expiring_soon(days=30)
for cert in expiring:
    print(f"{cert.name} expires in {cert.days_until_expiration()} days")

# Get statistics
stats = manager.get_statistics()
print(f"Total certificates: {stats['total']}")
print(f"Expired: {stats['expired']}")
```

## Testing

Run the test suite:

```bash
python -m unittest test_cert_manager.py -v
```

## Requirements

- Python 3.7 or higher
- cryptography >= 41.0.0
- python-dateutil >= 2.8.2
- tabulate >= 0.9.0 (for formatted table output)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/mattyys/cert-manager).
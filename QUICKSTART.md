# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/mattyys/cert-manager.git
cd cert-manager

# Install dependencies
pip install -r requirements.txt
```

## Quick Demo

Run the demo to see the certificate manager in action:

```bash
python demo.py
```

## Basic Usage

### 1. Add your first certificate

```bash
python cli.py add mysite example.com 2025-12-31 --issuer "Let's Encrypt"
```

### 2. List all certificates

```bash
python cli.py list
```

### 3. Check which certificates are expiring soon

```bash
python cli.py list --expiring-soon --days 30
```

### 4. View statistics

```bash
python cli.py stats
```

### 5. Update a certificate after renewal

```bash
python cli.py update mysite --expiration-date 2026-12-31
```

## Using as a Python Library

```python
from cert_manager import Certificate, CertificateManager

# Initialize manager
manager = CertificateManager()

# Add a certificate
cert = Certificate(
    name="mysite",
    domain="example.com",
    expiration_date="2025-12-31",
    issuer="Let's Encrypt"
)
manager.add_certificate(cert)

# Check for expiring certificates
expiring = manager.get_expiring_soon(days=30)
for cert in expiring:
    print(f"{cert.name} expires in {cert.days_until_expiration()} days")
```

## Common Tasks

### Monitor certificates expiring in the next 7 days

```bash
python cli.py list --expiring-soon --days 7
```

### Find all expired certificates

```bash
python cli.py list --expired
```

### Get detailed information about a certificate

```bash
python cli.py show mysite
```

### Remove a certificate

```bash
python cli.py remove mysite
```

## Tips

- Run `python cli.py stats` regularly to monitor your certificate health
- Set up a cron job to check for expiring certificates daily
- Use the `--storage` option to manage multiple certificate databases
- The default storage file is `certificates.json` in the current directory

## Need Help?

```bash
# Get help for all commands
python cli.py --help

# Get help for a specific command
python cli.py add --help
```

## Next Steps

- See `example_usage.py` for more Python API examples
- Check the full README.md for comprehensive documentation
- Run the test suite with `python -m unittest test_cert_manager.py -v`

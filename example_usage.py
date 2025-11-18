"""
Example: Using Certificate Manager as a Python library
This example shows how to use the Certificate Manager programmatically.
"""

from cert_manager import Certificate, CertificateManager
from datetime import datetime, timedelta

# Initialize the certificate manager
manager = CertificateManager(storage_file="my_certificates.json")

# Example 1: Add a new certificate
print("Example 1: Adding a certificate")
print("-" * 40)
cert = Certificate(
    name="my-website",
    domain="mywebsite.com",
    expiration_date="2025-12-31",
    issuer="Let's Encrypt",
    notes="Production SSL certificate"
)
manager.add_certificate(cert)
print(f"Added: {cert.name}")
print()

# Example 2: List all certificates
print("Example 2: Listing all certificates")
print("-" * 40)
for cert in manager.list_all_certificates():
    print(f"{cert.name}: {cert.domain} - Expires in {cert.days_until_expiration()} days")
print()

# Example 3: Check for expiring certificates
print("Example 3: Check for expiring certificates")
print("-" * 40)
expiring_soon = manager.get_expiring_soon(days=60)
if expiring_soon:
    print(f"Found {len(expiring_soon)} certificate(s) expiring in the next 60 days:")
    for cert in expiring_soon:
        print(f"  - {cert.name} ({cert.domain}) - {cert.days_until_expiration()} days left")
else:
    print("No certificates expiring in the next 60 days")
print()

# Example 4: Update a certificate
print("Example 4: Updating a certificate")
print("-" * 40)
manager.update_certificate(
    "my-website",
    expiration_date="2026-06-30",
    notes="Certificate renewed for another year"
)
updated_cert = manager.get_certificate("my-website")
print(f"Updated {updated_cert.name} - New expiration: {updated_cert.expiration_date}")
print()

# Example 5: Get statistics
print("Example 5: Certificate statistics")
print("-" * 40)
stats = manager.get_statistics()
print(f"Total certificates: {stats['total']}")
print(f"Valid certificates: {stats['valid']}")
print(f"Expired certificates: {stats['expired']}")
print(f"Expiring in 30 days: {stats['expiring_in_30_days']}")
print()

# Example 6: Check individual certificate status
print("Example 6: Check certificate status")
print("-" * 40)
cert = manager.get_certificate("my-website")
if cert:
    if cert.is_expired():
        print(f"⚠️  {cert.name} is EXPIRED!")
    elif cert.is_expiring_soon(30):
        print(f"⚠️  {cert.name} is expiring soon (within 30 days)")
    else:
        print(f"✓ {cert.name} is valid for {cert.days_until_expiration()} more days")
print()

# Clean up (optional)
# manager.remove_certificate("my-website")

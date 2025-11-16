#!/usr/bin/env python3
"""
Demo script for Certificate Manager
Demonstrates the functionality of the certificate management system.
"""

from datetime import datetime, timedelta
from cert_manager import Certificate, CertificateManager
import os

def demo():
    """Run a demonstration of the certificate manager."""
    print("=" * 80)
    print("Certificate Manager - Demo")
    print("=" * 80)
    print()
    
    # Use a temporary storage file for demo
    demo_storage = "/tmp/demo_certificates.json"
    if os.path.exists(demo_storage):
        os.remove(demo_storage)
    
    # Initialize manager
    print("1. Initializing Certificate Manager...")
    manager = CertificateManager(storage_file=demo_storage)
    print("   ✓ Manager initialized\n")
    
    # Add certificates with different expiration dates
    print("2. Adding certificates...")
    
    # Valid certificate (expires in 1 year)
    future_date_1y = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    cert1 = Certificate(
        name="production-web",
        domain="example.com",
        expiration_date=future_date_1y,
        issuer="Let's Encrypt",
        notes="Main production web server"
    )
    manager.add_certificate(cert1)
    print("   ✓ Added: production-web (expires in 1 year)")
    
    # Certificate expiring soon (15 days)
    expiring_date = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
    cert2 = Certificate(
        name="api-staging",
        domain="api-staging.example.com",
        expiration_date=expiring_date,
        issuer="DigiCert",
        notes="Staging API server - needs renewal"
    )
    manager.add_certificate(cert2)
    print("   ✓ Added: api-staging (expires in 15 days)")
    
    # Certificate expiring very soon (3 days)
    urgent_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    cert3 = Certificate(
        name="mail-server",
        domain="mail.example.com",
        expiration_date=urgent_date,
        issuer="Let's Encrypt",
        notes="Mail server - URGENT renewal required"
    )
    manager.add_certificate(cert3)
    print("   ✓ Added: mail-server (expires in 3 days)")
    
    # Expired certificate
    expired_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    cert4 = Certificate(
        name="old-service",
        domain="old.example.com",
        expiration_date=expired_date,
        issuer="Let's Encrypt",
        notes="Decommissioned service"
    )
    manager.add_certificate(cert4)
    print("   ✓ Added: old-service (already expired)\n")
    
    # Show all certificates
    print("3. Listing all certificates:")
    print("-" * 80)
    for cert in manager.list_all_certificates():
        days = cert.days_until_expiration()
        status = "EXPIRED" if days < 0 else f"{days} days remaining"
        print(f"   {cert.name:<20} {cert.domain:<30} {status}")
    print()
    
    # Show statistics
    print("4. Certificate Statistics:")
    print("-" * 80)
    stats = manager.get_statistics()
    print(f"   Total Certificates:          {stats['total']}")
    print(f"   Valid Certificates:          {stats['valid']}")
    print(f"   Expired Certificates:        {stats['expired']}")
    print(f"   Expiring in 7 days:         {stats['expiring_in_7_days']}")
    print(f"   Expiring in 30 days:        {stats['expiring_in_30_days']}")
    print()
    
    # Show expired certificates
    print("5. Expired Certificates:")
    print("-" * 80)
    expired = manager.get_expired_certificates()
    if expired:
        for cert in expired:
            print(f"   ⚠️  {cert.name} ({cert.domain}) - expired {abs(cert.days_until_expiration())} days ago")
    else:
        print("   No expired certificates")
    print()
    
    # Show expiring soon
    print("6. Certificates Expiring Soon (within 30 days):")
    print("-" * 80)
    expiring = manager.get_expiring_soon(30)
    if expiring:
        for cert in expiring:
            days = cert.days_until_expiration()
            urgency = "🔴 URGENT" if days <= 7 else "🟡 WARNING"
            print(f"   {urgency} {cert.name} ({cert.domain}) - {days} days remaining")
    else:
        print("   No certificates expiring soon")
    print()
    
    # Update a certificate
    print("7. Updating certificate (simulating renewal)...")
    new_expiry = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
    manager.update_certificate(
        "mail-server",
        expiration_date=new_expiry,
        notes="Certificate renewed - valid for 90 days"
    )
    updated_cert = manager.get_certificate("mail-server")
    print(f"   ✓ Updated: mail-server - now expires in {updated_cert.days_until_expiration()} days\n")
    
    # Show final statistics
    print("8. Updated Statistics:")
    print("-" * 80)
    stats = manager.get_statistics()
    print(f"   Expiring in 7 days:         {stats['expiring_in_7_days']}")
    print(f"   Expiring in 30 days:        {stats['expiring_in_30_days']}")
    print()
    
    # Clean up
    print("9. Cleaning up demo data...")
    if os.path.exists(demo_storage):
        os.remove(demo_storage)
    print("   ✓ Demo completed!\n")
    
    print("=" * 80)
    print("To use the certificate manager, run: python cli.py --help")
    print("=" * 80)


if __name__ == "__main__":
    demo()

#!/usr/bin/env python3
"""
Certificate Manager CLI
Command-line interface for managing certificate expiration dates.
"""

import argparse
import sys
from datetime import datetime
from cert_manager import Certificate, CertificateManager


def format_table(certificates, show_all=True):
    """Format certificates as a table."""
    if not certificates:
        return "No certificates found."
    
    try:
        from tabulate import tabulate
        
        headers = ["Name", "Domain", "Expiration Date", "Days Left", "Issuer", "Status"]
        rows = []
        
        for cert in certificates:
            days_left = cert.days_until_expiration()
            
            if cert.is_expired():
                status = "🔴 EXPIRED"
            elif cert.is_expiring_soon(7):
                status = "🟡 URGENT"
            elif cert.is_expiring_soon(30):
                status = "🟠 WARNING"
            else:
                status = "🟢 OK"
            
            rows.append([
                cert.name,
                cert.domain,
                cert.expiration_date.strftime("%Y-%m-%d"),
                days_left if days_left >= 0 else f"{days_left} (expired)",
                cert.issuer or "N/A",
                status
            ])
        
        return tabulate(rows, headers=headers, tablefmt="grid")
    except ImportError:
        # Fallback to simple formatting if tabulate is not available
        output = []
        for cert in certificates:
            output.append(str(cert))
        return "\n".join(output)


def cmd_add(args, manager):
    """Add a new certificate."""
    try:
        cert = Certificate(
            name=args.name,
            domain=args.domain,
            expiration_date=args.expiration_date,
            issuer=args.issuer or "",
            notes=args.notes or ""
        )
        manager.add_certificate(cert)
        print(f"✓ Certificate '{args.name}' added successfully.")
    except ValueError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_remove(args, manager):
    """Remove a certificate."""
    if manager.remove_certificate(args.name):
        print(f"✓ Certificate '{args.name}' removed successfully.")
    else:
        print(f"✗ Certificate '{args.name}' not found.", file=sys.stderr)
        sys.exit(1)


def cmd_list(args, manager):
    """List certificates."""
    if args.expired:
        certs = manager.get_expired_certificates()
        print("Expired Certificates:")
        print("=" * 80)
    elif args.expiring_soon:
        days = args.days or 30
        certs = manager.get_expiring_soon(days)
        print(f"Certificates Expiring in {days} Days:")
        print("=" * 80)
    else:
        certs = manager.list_all_certificates()
        print("All Certificates:")
        print("=" * 80)
    
    print(format_table(certs))


def cmd_update(args, manager):
    """Update a certificate."""
    updates = {}
    if args.domain:
        updates["domain"] = args.domain
    if args.expiration_date:
        updates["expiration_date"] = args.expiration_date
    if args.issuer:
        updates["issuer"] = args.issuer
    if args.notes:
        updates["notes"] = args.notes
    
    if not updates:
        print("✗ No updates specified.", file=sys.stderr)
        sys.exit(1)
    
    if manager.update_certificate(args.name, **updates):
        print(f"✓ Certificate '{args.name}' updated successfully.")
    else:
        print(f"✗ Certificate '{args.name}' not found.", file=sys.stderr)
        sys.exit(1)


def cmd_show(args, manager):
    """Show details of a specific certificate."""
    cert = manager.get_certificate(args.name)
    if not cert:
        print(f"✗ Certificate '{args.name}' not found.", file=sys.stderr)
        sys.exit(1)
    
    print(f"\nCertificate Details:")
    print("=" * 80)
    print(f"Name:            {cert.name}")
    print(f"Domain:          {cert.domain}")
    print(f"Expiration Date: {cert.expiration_date}")
    print(f"Days Left:       {cert.days_until_expiration()}")
    print(f"Issuer:          {cert.issuer or 'N/A'}")
    print(f"Notes:           {cert.notes or 'N/A'}")
    print(f"Status:          {'EXPIRED' if cert.is_expired() else 'Valid'}")
    print()


def cmd_stats(args, manager):
    """Show certificate statistics."""
    stats = manager.get_statistics()
    
    print("\nCertificate Statistics:")
    print("=" * 80)
    print(f"Total Certificates:           {stats['total']}")
    print(f"Valid Certificates:           {stats['valid']}")
    print(f"Expired Certificates:         {stats['expired']}")
    print(f"Expiring in 7 Days:          {stats['expiring_in_7_days']}")
    print(f"Expiring in 30 Days:         {stats['expiring_in_30_days']}")
    print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Certificate Manager - Track SSL/TLS certificate expiration dates",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--storage",
        default="certificates.json",
        help="Path to certificate storage file (default: certificates.json)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new certificate")
    parser_add.add_argument("name", help="Certificate name/identifier")
    parser_add.add_argument("domain", help="Domain name")
    parser_add.add_argument("expiration_date", help="Expiration date (YYYY-MM-DD)")
    parser_add.add_argument("--issuer", help="Certificate issuer")
    parser_add.add_argument("--notes", help="Additional notes")
    
    # Remove command
    parser_remove = subparsers.add_parser("remove", help="Remove a certificate")
    parser_remove.add_argument("name", help="Certificate name to remove")
    
    # List command
    parser_list = subparsers.add_parser("list", help="List certificates")
    parser_list.add_argument("--expired", action="store_true", help="Show only expired certificates")
    parser_list.add_argument("--expiring-soon", action="store_true", help="Show certificates expiring soon")
    parser_list.add_argument("--days", type=int, help="Number of days for expiring-soon filter (default: 30)")
    
    # Update command
    parser_update = subparsers.add_parser("update", help="Update a certificate")
    parser_update.add_argument("name", help="Certificate name to update")
    parser_update.add_argument("--domain", help="New domain name")
    parser_update.add_argument("--expiration-date", dest="expiration_date", help="New expiration date (YYYY-MM-DD)")
    parser_update.add_argument("--issuer", help="New issuer")
    parser_update.add_argument("--notes", help="New notes")
    
    # Show command
    parser_show = subparsers.add_parser("show", help="Show certificate details")
    parser_show.add_argument("name", help="Certificate name to show")
    
    # Stats command
    subparsers.add_parser("stats", help="Show certificate statistics")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize manager
    manager = CertificateManager(storage_file=args.storage)
    
    # Execute command
    commands = {
        "add": cmd_add,
        "remove": cmd_remove,
        "list": cmd_list,
        "update": cmd_update,
        "show": cmd_show,
        "stats": cmd_stats
    }
    
    commands[args.command](args, manager)


if __name__ == "__main__":
    main()

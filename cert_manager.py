"""
Certificate Manager - Mantenimiento de certificados (fechas de vencimientos)
A simple tool to manage and track SSL/TLS certificate expiration dates.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict
import json
import os
from pathlib import Path


class Certificate:
    """Represents an SSL/TLS certificate with expiration date tracking."""
    
    def __init__(self, name: str, domain: str, expiration_date: str, 
                 issuer: str = "", notes: str = ""):
        """
        Initialize a Certificate object.
        
        Args:
            name: Certificate identifier/name
            domain: Domain name for the certificate
            expiration_date: Expiration date in YYYY-MM-DD format
            issuer: Certificate issuer (e.g., Let's Encrypt, DigiCert)
            notes: Additional notes about the certificate
        """
        self.name = name
        self.domain = domain
        self.expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()
        self.issuer = issuer
        self.notes = notes
    
    def days_until_expiration(self) -> int:
        """Calculate days until certificate expiration."""
        today = datetime.now().date()
        delta = self.expiration_date - today
        return delta.days
    
    def is_expired(self) -> bool:
        """Check if certificate is expired."""
        return self.days_until_expiration() < 0
    
    def is_expiring_soon(self, days: int = 30) -> bool:
        """
        Check if certificate is expiring within specified days.
        
        Args:
            days: Number of days threshold (default 30)
        """
        days_left = self.days_until_expiration()
        return 0 <= days_left <= days
    
    def to_dict(self) -> Dict:
        """Convert certificate to dictionary format."""
        return {
            "name": self.name,
            "domain": self.domain,
            "expiration_date": self.expiration_date.strftime("%Y-%m-%d"),
            "issuer": self.issuer,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Certificate':
        """Create Certificate from dictionary."""
        return cls(
            name=data["name"],
            domain=data["domain"],
            expiration_date=data["expiration_date"],
            issuer=data.get("issuer", ""),
            notes=data.get("notes", "")
        )
    
    def __str__(self) -> str:
        days = self.days_until_expiration()
        status = "EXPIRED" if days < 0 else f"{days} days"
        return f"{self.name} ({self.domain}) - Expires: {self.expiration_date} ({status})"


class CertificateManager:
    """Manages a collection of certificates with expiration tracking."""
    
    def __init__(self, storage_file: str = "certificates.json"):
        """
        Initialize the CertificateManager.
        
        Args:
            storage_file: Path to JSON file for storing certificates
        """
        self.storage_file = storage_file
        self.certificates: List[Certificate] = []
        self.load_certificates()
    
    def add_certificate(self, certificate: Certificate) -> None:
        """Add a new certificate to the manager."""
        # Check for duplicate names
        if any(cert.name == certificate.name for cert in self.certificates):
            raise ValueError(f"Certificate with name '{certificate.name}' already exists")
        self.certificates.append(certificate)
        self.save_certificates()
    
    def remove_certificate(self, name: str) -> bool:
        """
        Remove a certificate by name.
        
        Returns:
            True if certificate was removed, False if not found
        """
        initial_count = len(self.certificates)
        self.certificates = [cert for cert in self.certificates if cert.name != name]
        if len(self.certificates) < initial_count:
            self.save_certificates()
            return True
        return False
    
    def get_certificate(self, name: str) -> Optional[Certificate]:
        """Get a certificate by name."""
        for cert in self.certificates:
            if cert.name == name:
                return cert
        return None
    
    def update_certificate(self, name: str, **kwargs) -> bool:
        """
        Update certificate attributes.
        
        Args:
            name: Certificate name to update
            **kwargs: Attributes to update (domain, expiration_date, issuer, notes)
        
        Returns:
            True if updated, False if certificate not found
        """
        cert = self.get_certificate(name)
        if not cert:
            return False
        
        if "domain" in kwargs:
            cert.domain = kwargs["domain"]
        if "expiration_date" in kwargs:
            cert.expiration_date = datetime.strptime(kwargs["expiration_date"], "%Y-%m-%d").date()
        if "issuer" in kwargs:
            cert.issuer = kwargs["issuer"]
        if "notes" in kwargs:
            cert.notes = kwargs["notes"]
        
        self.save_certificates()
        return True
    
    def list_all_certificates(self) -> List[Certificate]:
        """Get all certificates."""
        return self.certificates
    
    def get_expired_certificates(self) -> List[Certificate]:
        """Get all expired certificates."""
        return [cert for cert in self.certificates if cert.is_expired()]
    
    def get_expiring_soon(self, days: int = 30) -> List[Certificate]:
        """
        Get certificates expiring within specified days.
        
        Args:
            days: Number of days threshold (default 30)
        """
        return [cert for cert in self.certificates if cert.is_expiring_soon(days)]
    
    def save_certificates(self) -> None:
        """Save certificates to JSON file."""
        data = [cert.to_dict() for cert in self.certificates]
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_certificates(self) -> None:
        """Load certificates from JSON file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.certificates = [Certificate.from_dict(cert_data) for cert_data in data]
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Error loading certificates: {e}")
                self.certificates = []
        else:
            self.certificates = []
    
    def get_statistics(self) -> Dict:
        """Get statistics about certificates."""
        total = len(self.certificates)
        expired = len(self.get_expired_certificates())
        expiring_30 = len(self.get_expiring_soon(30))
        expiring_7 = len(self.get_expiring_soon(7))
        
        return {
            "total": total,
            "expired": expired,
            "expiring_in_30_days": expiring_30,
            "expiring_in_7_days": expiring_7,
            "valid": total - expired
        }

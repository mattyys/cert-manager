"""
Unit tests for Certificate Manager
Tests certificate expiration date tracking functionality.
"""

import unittest
import os
import json
import tempfile
from datetime import datetime, timedelta
from cert_manager import Certificate, CertificateManager


class TestCertificate(unittest.TestCase):
    """Test Certificate class functionality."""
    
    def test_certificate_creation(self):
        """Test creating a certificate."""
        cert = Certificate(
            name="test-cert",
            domain="example.com",
            expiration_date="2025-12-31",
            issuer="Let's Encrypt",
            notes="Test certificate"
        )
        
        self.assertEqual(cert.name, "test-cert")
        self.assertEqual(cert.domain, "example.com")
        self.assertEqual(cert.issuer, "Let's Encrypt")
        self.assertEqual(cert.notes, "Test certificate")
    
    def test_days_until_expiration(self):
        """Test calculating days until expiration."""
        # Create a certificate expiring in 30 days
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        cert = Certificate("test", "example.com", future_date)
        
        days = cert.days_until_expiration()
        self.assertEqual(days, 30)
    
    def test_is_expired(self):
        """Test expired certificate detection."""
        # Past date
        past_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        cert_expired = Certificate("expired", "example.com", past_date)
        self.assertTrue(cert_expired.is_expired())
        
        # Future date
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        cert_valid = Certificate("valid", "example.com", future_date)
        self.assertFalse(cert_valid.is_expired())
    
    def test_is_expiring_soon(self):
        """Test expiring soon detection."""
        # Certificate expiring in 15 days
        date_15_days = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
        cert = Certificate("soon", "example.com", date_15_days)
        
        self.assertTrue(cert.is_expiring_soon(30))
        self.assertTrue(cert.is_expiring_soon(15))
        self.assertFalse(cert.is_expiring_soon(10))
    
    def test_to_dict(self):
        """Test converting certificate to dictionary."""
        cert = Certificate(
            name="test-cert",
            domain="example.com",
            expiration_date="2025-12-31",
            issuer="Let's Encrypt",
            notes="Test"
        )
        
        cert_dict = cert.to_dict()
        self.assertEqual(cert_dict["name"], "test-cert")
        self.assertEqual(cert_dict["domain"], "example.com")
        self.assertEqual(cert_dict["expiration_date"], "2025-12-31")
        self.assertEqual(cert_dict["issuer"], "Let's Encrypt")
        self.assertEqual(cert_dict["notes"], "Test")
    
    def test_from_dict(self):
        """Test creating certificate from dictionary."""
        data = {
            "name": "test-cert",
            "domain": "example.com",
            "expiration_date": "2025-12-31",
            "issuer": "Let's Encrypt",
            "notes": "Test"
        }
        
        cert = Certificate.from_dict(data)
        self.assertEqual(cert.name, "test-cert")
        self.assertEqual(cert.domain, "example.com")
        self.assertEqual(cert.issuer, "Let's Encrypt")


class TestCertificateManager(unittest.TestCase):
    """Test CertificateManager class functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.manager = CertificateManager(storage_file=self.temp_file.name)
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_certificate(self):
        """Test adding a certificate."""
        cert = Certificate("test", "example.com", "2025-12-31")
        self.manager.add_certificate(cert)
        
        self.assertEqual(len(self.manager.certificates), 1)
        self.assertEqual(self.manager.certificates[0].name, "test")
    
    def test_add_duplicate_certificate(self):
        """Test adding duplicate certificate raises error."""
        cert1 = Certificate("test", "example.com", "2025-12-31")
        cert2 = Certificate("test", "other.com", "2025-12-31")
        
        self.manager.add_certificate(cert1)
        with self.assertRaises(ValueError):
            self.manager.add_certificate(cert2)
    
    def test_remove_certificate(self):
        """Test removing a certificate."""
        cert = Certificate("test", "example.com", "2025-12-31")
        self.manager.add_certificate(cert)
        
        result = self.manager.remove_certificate("test")
        self.assertTrue(result)
        self.assertEqual(len(self.manager.certificates), 0)
    
    def test_remove_nonexistent_certificate(self):
        """Test removing non-existent certificate."""
        result = self.manager.remove_certificate("nonexistent")
        self.assertFalse(result)
    
    def test_get_certificate(self):
        """Test retrieving a certificate."""
        cert = Certificate("test", "example.com", "2025-12-31")
        self.manager.add_certificate(cert)
        
        retrieved = self.manager.get_certificate("test")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "test")
    
    def test_get_nonexistent_certificate(self):
        """Test retrieving non-existent certificate."""
        retrieved = self.manager.get_certificate("nonexistent")
        self.assertIsNone(retrieved)
    
    def test_update_certificate(self):
        """Test updating certificate attributes."""
        cert = Certificate("test", "example.com", "2025-12-31")
        self.manager.add_certificate(cert)
        
        result = self.manager.update_certificate(
            "test",
            domain="newdomain.com",
            issuer="New Issuer"
        )
        
        self.assertTrue(result)
        updated = self.manager.get_certificate("test")
        self.assertEqual(updated.domain, "newdomain.com")
        self.assertEqual(updated.issuer, "New Issuer")
    
    def test_list_all_certificates(self):
        """Test listing all certificates."""
        cert1 = Certificate("test1", "example1.com", "2025-12-31")
        cert2 = Certificate("test2", "example2.com", "2025-12-31")
        
        self.manager.add_certificate(cert1)
        self.manager.add_certificate(cert2)
        
        all_certs = self.manager.list_all_certificates()
        self.assertEqual(len(all_certs), 2)
    
    def test_get_expired_certificates(self):
        """Test getting expired certificates."""
        past_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        
        cert_expired = Certificate("expired", "example.com", past_date)
        cert_valid = Certificate("valid", "example.com", future_date)
        
        self.manager.add_certificate(cert_expired)
        self.manager.add_certificate(cert_valid)
        
        expired = self.manager.get_expired_certificates()
        self.assertEqual(len(expired), 1)
        self.assertEqual(expired[0].name, "expired")
    
    def test_get_expiring_soon(self):
        """Test getting certificates expiring soon."""
        date_15_days = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
        date_60_days = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
        
        cert_soon = Certificate("soon", "example.com", date_15_days)
        cert_later = Certificate("later", "example.com", date_60_days)
        
        self.manager.add_certificate(cert_soon)
        self.manager.add_certificate(cert_later)
        
        expiring_30 = self.manager.get_expiring_soon(30)
        self.assertEqual(len(expiring_30), 1)
        self.assertEqual(expiring_30[0].name, "soon")
    
    def test_save_and_load_certificates(self):
        """Test saving and loading certificates from file."""
        cert = Certificate("test", "example.com", "2025-12-31", "Let's Encrypt", "Notes")
        self.manager.add_certificate(cert)
        
        # Create new manager instance with same file
        new_manager = CertificateManager(storage_file=self.temp_file.name)
        
        self.assertEqual(len(new_manager.certificates), 1)
        loaded = new_manager.get_certificate("test")
        self.assertEqual(loaded.name, "test")
        self.assertEqual(loaded.domain, "example.com")
        self.assertEqual(loaded.issuer, "Let's Encrypt")
    
    def test_get_statistics(self):
        """Test getting certificate statistics."""
        past_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        date_5_days = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        date_20_days = (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d")
        date_60_days = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
        
        self.manager.add_certificate(Certificate("expired", "example.com", past_date))
        self.manager.add_certificate(Certificate("urgent", "example.com", date_5_days))
        self.manager.add_certificate(Certificate("warning", "example.com", date_20_days))
        self.manager.add_certificate(Certificate("ok", "example.com", date_60_days))
        
        stats = self.manager.get_statistics()
        
        self.assertEqual(stats["total"], 4)
        self.assertEqual(stats["expired"], 1)
        self.assertEqual(stats["expiring_in_7_days"], 1)
        self.assertEqual(stats["expiring_in_30_days"], 2)
        self.assertEqual(stats["valid"], 3)


if __name__ == "__main__":
    unittest.main()

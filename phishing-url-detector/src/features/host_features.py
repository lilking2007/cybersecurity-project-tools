"""
Host-Based Feature Extraction

Extracts features related to domain registration, WHOIS data, and SSL certificates.
"""

import socket
import ssl
import whois
import dns.resolver
from datetime import datetime, timezone
from typing import Dict, Optional
import requests
from OpenSSL import crypto


class HostBasedFeatureExtractor:
    """Extract host-based features from URLs."""
    
    def __init__(self, whois_timeout: int = 5, dns_timeout: int = 3):
        """
        Initialize host-based feature extractor.
        
        Args:
            whois_timeout: Timeout for WHOIS queries
            dns_timeout: Timeout for DNS queries
        """
        self.whois_timeout = whois_timeout
        self.dns_timeout = dns_timeout
        self.dns_resolver = dns.resolver.Resolver()
        self.dns_resolver.timeout = dns_timeout
        self.dns_resolver.lifetime = dns_timeout
    
    def extract(self, parsed_data: Dict) -> Dict[str, any]:
        """
        Extract all host-based features.
        
        Args:
            parsed_data: Parsed URL components
            
        Returns:
            Dictionary of host-based features
        """
        features = {}
        hostname = parsed_data['hostname']
        
        if not hostname:
            return self._get_default_features()
        
        # Extract WHOIS features
        whois_features = self._extract_whois_features(hostname)
        features.update(whois_features)
        
        # Extract DNS features
        dns_features = self._extract_dns_features(hostname)
        features.update(dns_features)
        
        # Extract SSL certificate features
        if parsed_data['scheme'] == 'https':
            ssl_features = self._extract_ssl_features(hostname, parsed_data.get('port', 443))
            features.update(ssl_features)
        else:
            features.update(self._get_default_ssl_features())
        
        return features
    
    def _extract_whois_features(self, hostname: str) -> Dict[str, any]:
        """Extract WHOIS-based features."""
        features = {
            'whois_domain_age_days': -1,
            'whois_domain_age_months': -1,
            'whois_registrar_known': False,
            'whois_privacy_protected': False,
            'whois_days_until_expiry': -1,
            'whois_query_success': False
        }
        
        try:
            w = whois.whois(hostname)
            
            # Domain age
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            
            if creation_date:
                # Ensure timezone-aware datetime
                if creation_date.tzinfo is None:
                    creation_date = creation_date.replace(tzinfo=timezone.utc)
                
                now = datetime.now(timezone.utc)
                age = now - creation_date
                features['whois_domain_age_days'] = age.days
                features['whois_domain_age_months'] = age.days / 30.44
                features['whois_query_success'] = True
            
            # Expiration date
            expiration_date = w.expiration_date
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
            
            if expiration_date:
                if expiration_date.tzinfo is None:
                    expiration_date = expiration_date.replace(tzinfo=timezone.utc)
                
                now = datetime.now(timezone.utc)
                days_until_expiry = (expiration_date - now).days
                features['whois_days_until_expiry'] = days_until_expiry
            
            # Registrar
            if w.registrar:
                features['whois_registrar_known'] = True
                # Check for privacy protection services
                privacy_keywords = ['privacy', 'protect', 'proxy', 'whoisguard', 'private']
                registrar_lower = str(w.registrar).lower()
                features['whois_privacy_protected'] = any(kw in registrar_lower for kw in privacy_keywords)
            
        except Exception as e:
            # WHOIS query failed - suspicious indicator
            features['whois_query_success'] = False
        
        return features
    
    def _extract_dns_features(self, hostname: str) -> Dict[str, any]:
        """Extract DNS-based features."""
        features = {
            'dns_a_record_count': 0,
            'dns_mx_record_count': 0,
            'dns_ns_record_count': 0,
            'dns_txt_record_count': 0,
            'dns_has_spf': False,
            'dns_has_dmarc': False,
            'dns_query_success': False,
            'dns_ip_addresses': []
        }
        
        try:
            # A records (IPv4)
            try:
                a_records = self.dns_resolver.resolve(hostname, 'A')
                features['dns_a_record_count'] = len(a_records)
                features['dns_ip_addresses'] = [str(r) for r in a_records]
                features['dns_query_success'] = True
            except:
                pass
            
            # MX records (mail servers)
            try:
                mx_records = self.dns_resolver.resolve(hostname, 'MX')
                features['dns_mx_record_count'] = len(mx_records)
            except:
                pass
            
            # NS records (name servers)
            try:
                ns_records = self.dns_resolver.resolve(hostname, 'NS')
                features['dns_ns_record_count'] = len(ns_records)
            except:
                pass
            
            # TXT records (SPF, DMARC, etc.)
            try:
                txt_records = self.dns_resolver.resolve(hostname, 'TXT')
                features['dns_txt_record_count'] = len(txt_records)
                
                # Check for SPF and DMARC
                for record in txt_records:
                    record_str = str(record).lower()
                    if 'v=spf1' in record_str:
                        features['dns_has_spf'] = True
                    if 'v=dmarc1' in record_str:
                        features['dns_has_dmarc'] = True
            except:
                pass
            
        except Exception as e:
            features['dns_query_success'] = False
        
        return features
    
    def _extract_ssl_features(self, hostname: str, port: int = 443) -> Dict[str, any]:
        """Extract SSL certificate features."""
        features = {
            'ssl_valid': False,
            'ssl_issuer_known': False,
            'ssl_self_signed': False,
            'ssl_days_until_expiry': -1,
            'ssl_certificate_age_days': -1,
            'ssl_common_name_match': False,
            'ssl_wildcard': False
        }
        
        try:
            # Create SSL context
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # Get certificate
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert_der = ssock.getpeercert(binary_form=True)
                    cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_der)
                    
                    # Certificate validity
                    features['ssl_valid'] = True
                    
                    # Expiration date
                    expiry_date = datetime.strptime(
                        cert.get_notAfter().decode('ascii'),
                        '%Y%m%d%H%M%SZ'
                    ).replace(tzinfo=timezone.utc)
                    
                    now = datetime.now(timezone.utc)
                    features['ssl_days_until_expiry'] = (expiry_date - now).days
                    
                    # Issue date
                    issue_date = datetime.strptime(
                        cert.get_notBefore().decode('ascii'),
                        '%Y%m%d%H%M%SZ'
                    ).replace(tzinfo=timezone.utc)
                    
                    features['ssl_certificate_age_days'] = (now - issue_date).days
                    
                    # Issuer
                    issuer = cert.get_issuer()
                    issuer_cn = issuer.CN if hasattr(issuer, 'CN') else None
                    
                    # Known certificate authorities
                    known_cas = [
                        'Let\'s Encrypt', 'DigiCert', 'GeoTrust', 'Comodo',
                        'GlobalSign', 'Symantec', 'Thawte', 'RapidSSL',
                        'GoDaddy', 'Entrust'
                    ]
                    
                    if issuer_cn:
                        features['ssl_issuer_known'] = any(ca.lower() in issuer_cn.lower() for ca in known_cas)
                    
                    # Check if self-signed
                    subject = cert.get_subject()
                    features['ssl_self_signed'] = (subject == issuer)
                    
                    # Common name match
                    subject_cn = subject.CN if hasattr(subject, 'CN') else None
                    if subject_cn:
                        features['ssl_common_name_match'] = (hostname in subject_cn or subject_cn in hostname)
                        features['ssl_wildcard'] = subject_cn.startswith('*.')
            
        except Exception as e:
            # SSL connection failed
            features['ssl_valid'] = False
        
        return features
    
    def _get_default_features(self) -> Dict[str, any]:
        """Get default features when hostname is invalid."""
        features = self._get_default_ssl_features()
        features.update({
            'whois_domain_age_days': -1,
            'whois_domain_age_months': -1,
            'whois_registrar_known': False,
            'whois_privacy_protected': False,
            'whois_days_until_expiry': -1,
            'whois_query_success': False,
            'dns_a_record_count': 0,
            'dns_mx_record_count': 0,
            'dns_ns_record_count': 0,
            'dns_txt_record_count': 0,
            'dns_has_spf': False,
            'dns_has_dmarc': False,
            'dns_query_success': False,
            'dns_ip_addresses': []
        })
        return features
    
    def _get_default_ssl_features(self) -> Dict[str, any]:
        """Get default SSL features."""
        return {
            'ssl_valid': False,
            'ssl_issuer_known': False,
            'ssl_self_signed': False,
            'ssl_days_until_expiry': -1,
            'ssl_certificate_age_days': -1,
            'ssl_common_name_match': False,
            'ssl_wildcard': False
        }

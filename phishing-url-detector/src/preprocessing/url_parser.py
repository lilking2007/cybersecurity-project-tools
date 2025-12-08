"""
URL Preprocessing Module

Handles URL parsing, validation, and sanitization.
"""

import re
import validators
from urllib.parse import urlparse, parse_qs
from typing import Dict, Optional, Tuple
import tldextract


class URLPreprocessor:
    """Preprocess and parse URLs for feature extraction."""
    
    def __init__(self, max_length: int = 2048):
        """
        Initialize URL preprocessor.
        
        Args:
            max_length: Maximum allowed URL length
        """
        self.max_length = max_length
        self.suspicious_keywords = [
            'login', 'verify', 'account', 'update', 'secure', 'banking',
            'paypal', 'ebay', 'amazon', 'signin', 'confirm', 'suspended',
            'locked', 'unusual', 'activity', 'click', 'here', 'now',
            'urgent', 'immediately', 'expire', 'password', 'credential'
        ]
    
    def sanitize(self, url: str) -> str:
        """
        Sanitize URL by removing dangerous characters and normalizing.
        
        Args:
            url: Raw URL string
            
        Returns:
            Sanitized URL
        """
        # Strip whitespace
        url = url.strip()
        
        # Remove common URL encoding issues
        url = url.replace(' ', '%20')
        
        # Ensure scheme exists
        if not url.startswith(('http://', 'https://', 'ftp://')):
            url = 'http://' + url
        
        return url
    
    def validate(self, url: str) -> Tuple[bool, Optional[str]]:
        """
        Validate URL format and safety.
        
        Args:
            url: URL to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check length
        if len(url) > self.max_length:
            return False, f"URL exceeds maximum length of {self.max_length}"
        
        # Check if valid URL format
        if not validators.url(url):
            return False, "Invalid URL format"
        
        # Parse URL
        parsed = urlparse(url)
        
        # Check scheme
        if parsed.scheme not in ['http', 'https']:
            return False, f"Unsupported URL scheme: {parsed.scheme}"
        
        # Check for localhost/internal IPs (optional security check)
        if parsed.hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
            return False, "Localhost URLs not allowed"
        
        return True, None
    
    def parse(self, url: str) -> Dict[str, any]:
        """
        Parse URL into components for feature extraction.
        
        Args:
            url: URL to parse
            
        Returns:
            Dictionary containing parsed URL components
        """
        # Sanitize first
        url = self.sanitize(url)
        
        # Validate
        is_valid, error = self.validate(url)
        if not is_valid:
            raise ValueError(f"Invalid URL: {error}")
        
        # Parse with urllib
        parsed = urlparse(url)
        
        # Extract domain components with tldextract
        ext = tldextract.extract(url)
        
        # Parse query parameters
        query_params = parse_qs(parsed.query)
        
        return {
            'original_url': url,
            'scheme': parsed.scheme,
            'hostname': parsed.hostname,
            'port': parsed.port,
            'path': parsed.path,
            'query': parsed.query,
            'fragment': parsed.fragment,
            'domain': ext.domain,
            'subdomain': ext.subdomain,
            'suffix': ext.suffix,
            'registered_domain': ext.registered_domain,
            'fqdn': ext.fqdn,
            'query_params': query_params,
            'username': parsed.username,
            'password': parsed.password
        }
    
    def extract_suspicious_patterns(self, url: str) -> Dict[str, any]:
        """
        Extract suspicious patterns from URL.
        
        Args:
            url: URL to analyze
            
        Returns:
            Dictionary of suspicious pattern indicators
        """
        url_lower = url.lower()
        
        # Check for suspicious keywords
        found_keywords = [kw for kw in self.suspicious_keywords if kw in url_lower]
        
        # Check for IP address in hostname
        parsed = urlparse(url)
        is_ip = self._is_ip_address(parsed.hostname)
        
        # Check for @ symbol (username in URL)
        has_at_symbol = '@' in url
        
        # Check for excessive subdomains
        ext = tldextract.extract(url)
        subdomain_count = len(ext.subdomain.split('.')) if ext.subdomain else 0
        
        # Check for URL shorteners
        shortener_domains = [
            'bit.ly', 'goo.gl', 't.co', 'tinyurl.com', 'ow.ly',
            'buff.ly', 'is.gd', 'tiny.cc', 'cli.gs'
        ]
        is_shortened = ext.registered_domain in shortener_domains
        
        # Check for homograph attacks (Unicode confusables)
        has_unicode = not url.isascii()
        
        # Check for excessive special characters
        special_char_count = sum(1 for c in url if c in '-_.~!*\'();:@&=+$,/?#[]')
        special_char_ratio = special_char_count / len(url) if len(url) > 0 else 0
        
        return {
            'suspicious_keywords': found_keywords,
            'suspicious_keyword_count': len(found_keywords),
            'is_ip_address': is_ip,
            'has_at_symbol': has_at_symbol,
            'subdomain_count': subdomain_count,
            'is_url_shortener': is_shortened,
            'has_unicode_chars': has_unicode,
            'special_char_count': special_char_count,
            'special_char_ratio': special_char_ratio
        }
    
    def _is_ip_address(self, hostname: str) -> bool:
        """Check if hostname is an IP address."""
        if not hostname:
            return False
        
        # IPv4 pattern
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ipv4_pattern, hostname):
            return True
        
        # IPv6 pattern (simplified)
        if ':' in hostname:
            return True
        
        return False

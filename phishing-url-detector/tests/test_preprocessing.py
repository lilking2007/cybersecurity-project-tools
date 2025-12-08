"""
Unit tests for URL preprocessing module.
"""

import pytest
from src.preprocessing.url_parser import URLPreprocessor


class TestURLPreprocessor:
    """Test URL preprocessing functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.preprocessor = URLPreprocessor()
    
    def test_sanitize_adds_scheme(self):
        """Test that sanitize adds http:// if missing."""
        url = "example.com"
        sanitized = self.preprocessor.sanitize(url)
        assert sanitized.startswith('http://')
    
    def test_sanitize_preserves_https(self):
        """Test that sanitize preserves https://."""
        url = "https://example.com"
        sanitized = self.preprocessor.sanitize(url)
        assert sanitized.startswith('https://')
    
    def test_validate_rejects_localhost(self):
        """Test that validate rejects localhost URLs."""
        url = "http://localhost/test"
        is_valid, error = self.preprocessor.validate(url)
        assert not is_valid
        assert "localhost" in error.lower()
    
    def test_validate_accepts_valid_url(self):
        """Test that validate accepts valid URLs."""
        url = "https://www.example.com"
        is_valid, error = self.preprocessor.validate(url)
        assert is_valid
        assert error is None
    
    def test_parse_extracts_components(self):
        """Test that parse extracts URL components."""
        url = "https://subdomain.example.com:8080/path?query=value#fragment"
        parsed = self.preprocessor.parse(url)
        
        assert parsed['scheme'] == 'https'
        assert parsed['hostname'] == 'subdomain.example.com'
        assert parsed['port'] == 8080
        assert parsed['path'] == '/path'
        assert parsed['query'] == 'query=value'
        assert parsed['fragment'] == 'fragment'
    
    def test_extract_suspicious_patterns_detects_keywords(self):
        """Test suspicious keyword detection."""
        url = "http://paypal-verify-account.com/login"
        patterns = self.preprocessor.extract_suspicious_patterns(url)
        
        assert patterns['suspicious_keyword_count'] > 0
        assert 'verify' in [kw.lower() for kw in patterns['suspicious_keywords']]
    
    def test_extract_suspicious_patterns_detects_ip(self):
        """Test IP address detection."""
        url = "http://192.168.1.1/test"
        patterns = self.preprocessor.extract_suspicious_patterns(url)
        
        assert patterns['is_ip_address'] is True
    
    def test_extract_suspicious_patterns_detects_at_symbol(self):
        """Test @ symbol detection."""
        url = "http://user@example.com/test"
        patterns = self.preprocessor.extract_suspicious_patterns(url)
        
        assert patterns['has_at_symbol'] is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

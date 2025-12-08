"""
Network Feature Extraction

Extracts network-based features including redirects, geolocation, and ASN information.
"""

import requests
import socket
from typing import Dict, List, Optional
from urllib.parse import urlparse


class NetworkFeatureExtractor:
    """Extract network-based features from URLs."""
    
    def __init__(self, request_timeout: int = 10, max_redirects: int = 5):
        """
        Initialize network feature extractor.
        
        Args:
            request_timeout: Timeout for HTTP requests
            max_redirects: Maximum number of redirects to follow
        """
        self.request_timeout = request_timeout
        self.max_redirects = max_redirects
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract(self, url: str, parsed_data: Dict) -> Dict[str, any]:
        """
        Extract all network-based features.
        
        Args:
            url: Original URL
            parsed_data: Parsed URL components
            
        Returns:
            Dictionary of network features
        """
        features = {}
        
        # Extract redirect features
        redirect_features = self._extract_redirect_features(url)
        features.update(redirect_features)
        
        # Extract IP geolocation features (basic)
        geo_features = self._extract_geo_features(parsed_data['hostname'])
        features.update(geo_features)
        
        # Extract response features
        response_features = self._extract_response_features(url)
        features.update(response_features)
        
        return features
    
    def _extract_redirect_features(self, url: str) -> Dict[str, any]:
        """Extract redirect chain features."""
        features = {
            'redirect_count': 0,
            'redirect_chain_length': 0,
            'has_redirects': False,
            'redirect_to_different_domain': False,
            'redirect_urls': [],
            'final_url': url
        }
        
        try:
            # Follow redirects
            response = self.session.get(
                url,
                allow_redirects=True,
                timeout=self.request_timeout,
                verify=False  # Don't verify SSL for analysis
            )
            
            # Analyze redirect history
            if response.history:
                features['has_redirects'] = True
                features['redirect_count'] = len(response.history)
                features['redirect_chain_length'] = len(response.history)
                features['redirect_urls'] = [r.url for r in response.history]
                features['final_url'] = response.url
                
                # Check if redirected to different domain
                original_domain = urlparse(url).netloc
                final_domain = urlparse(response.url).netloc
                features['redirect_to_different_domain'] = (original_domain != final_domain)
            
        except Exception as e:
            # Request failed - could be suspicious
            pass
        
        return features
    
    def _extract_geo_features(self, hostname: str) -> Dict[str, any]:
        """Extract IP geolocation features."""
        features = {
            'ip_address': None,
            'ip_is_private': False,
            'ip_resolved': False
        }
        
        if not hostname:
            return features
        
        try:
            # Resolve hostname to IP
            ip_address = socket.gethostbyname(hostname)
            features['ip_address'] = ip_address
            features['ip_resolved'] = True
            
            # Check if private IP
            features['ip_is_private'] = self._is_private_ip(ip_address)
            
        except Exception as e:
            features['ip_resolved'] = False
        
        return features
    
    def _extract_response_features(self, url: str) -> Dict[str, any]:
        """Extract HTTP response features."""
        features = {
            'response_status_code': -1,
            'response_time_ms': -1,
            'response_size_bytes': -1,
            'has_favicon': False,
            'request_success': False
        }
        
        try:
            import time
            start_time = time.time()
            
            response = self.session.get(
                url,
                timeout=self.request_timeout,
                verify=False,
                allow_redirects=True
            )
            
            end_time = time.time()
            
            features['response_status_code'] = response.status_code
            features['response_time_ms'] = int((end_time - start_time) * 1000)
            features['response_size_bytes'] = len(response.content)
            features['request_success'] = True
            
            # Check for favicon
            if response.status_code == 200:
                content_lower = response.text.lower()
                features['has_favicon'] = 'favicon' in content_lower
            
        except Exception as e:
            features['request_success'] = False
        
        return features
    
    def _is_private_ip(self, ip: str) -> bool:
        """Check if IP address is private."""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            
            first_octet = int(parts[0])
            second_octet = int(parts[1])
            
            # Private IP ranges
            if first_octet == 10:
                return True
            if first_octet == 172 and 16 <= second_octet <= 31:
                return True
            if first_octet == 192 and second_octet == 168:
                return True
            if first_octet == 127:  # Loopback
                return True
            
            return False
        except:
            return False

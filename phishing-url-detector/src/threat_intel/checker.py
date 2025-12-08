"""
Threat Intelligence Integration

Integrates with external threat intelligence sources for URL reputation checking.
"""

import requests
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import hashlib


class ThreatIntelligenceChecker:
    """Check URLs against threat intelligence sources."""
    
    def __init__(self, config: Dict):
        """
        Initialize threat intelligence checker.
        
        Args:
            config: Configuration dictionary with API keys and settings
        """
        self.config = config
        self.cache = {}  # Simple in-memory cache
        self.cache_ttl = 3600  # 1 hour default
    
    def check_all(self, url: str) -> Dict[str, any]:
        """
        Check URL against all enabled threat intelligence sources.
        
        Args:
            url: URL to check
            
        Returns:
            Dictionary with threat intelligence results
        """
        results = {
            'is_malicious': False,
            'threat_sources': [],
            'threat_score': 0.0,
            'details': {}
        }
        
        # Check PhishTank
        if self.config.get('threat_intel', {}).get('phishtank', {}).get('enabled'):
            phishtank_result = self._check_phishtank(url)
            if phishtank_result['is_malicious']:
                results['is_malicious'] = True
                results['threat_sources'].append('PhishTank')
                results['details']['phishtank'] = phishtank_result
        
        # Check URLhaus
        if self.config.get('threat_intel', {}).get('urlhaus', {}).get('enabled'):
            urlhaus_result = self._check_urlhaus(url)
            if urlhaus_result['is_malicious']:
                results['is_malicious'] = True
                results['threat_sources'].append('URLhaus')
                results['details']['urlhaus'] = urlhaus_result
        
        # Check OpenPhish
        if self.config.get('threat_intel', {}).get('openphish', {}).get('enabled'):
            openphish_result = self._check_openphish(url)
            if openphish_result['is_malicious']:
                results['is_malicious'] = True
                results['threat_sources'].append('OpenPhish')
                results['details']['openphish'] = openphish_result
        
        # Calculate overall threat score
        if results['threat_sources']:
            results['threat_score'] = min(1.0, len(results['threat_sources']) * 0.4)
        
        return results
    
    def _check_phishtank(self, url: str) -> Dict[str, any]:
        """Check URL against PhishTank database."""
        result = {
            'is_malicious': False,
            'verified': False,
            'submission_time': None
        }
        
        # Check cache first
        cache_key = f'phishtank_{hashlib.md5(url.encode()).hexdigest()}'
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if time.time() - cached['timestamp'] < self.cache_ttl:
                return cached['data']
        
        try:
            api_key = self.config.get('threat_intel', {}).get('phishtank', {}).get('api_key')
            if not api_key:
                return result
            
            # PhishTank API endpoint
            api_url = 'https://checkurl.phishtank.com/checkurl/'
            
            data = {
                'url': url,
                'format': 'json',
                'app_key': api_key
            }
            
            response = requests.post(api_url, data=data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and data['results'].get('in_database'):
                    result['is_malicious'] = True
                    result['verified'] = data['results'].get('verified', False)
                    result['submission_time'] = data['results'].get('submission_time')
            
            # Cache result
            self.cache[cache_key] = {
                'timestamp': time.time(),
                'data': result
            }
            
        except Exception as e:
            # API call failed, return negative result
            pass
        
        return result
    
    def _check_urlhaus(self, url: str) -> Dict[str, any]:
        """Check URL against URLhaus database."""
        result = {
            'is_malicious': False,
            'threat_type': None,
            'tags': []
        }
        
        # Check cache
        cache_key = f'urlhaus_{hashlib.md5(url.encode()).hexdigest()}'
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if time.time() - cached['timestamp'] < self.cache_ttl:
                return cached['data']
        
        try:
            api_url = 'https://urlhaus-api.abuse.ch/v1/url/'
            
            data = {'url': url}
            response = requests.post(api_url, data=data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('query_status') == 'ok':
                    result['is_malicious'] = True
                    result['threat_type'] = data.get('threat')
                    result['tags'] = data.get('tags', [])
            
            # Cache result
            self.cache[cache_key] = {
                'timestamp': time.time(),
                'data': result
            }
            
        except Exception as e:
            pass
        
        return result
    
    def _check_openphish(self, url: str) -> Dict[str, any]:
        """Check URL against OpenPhish feed."""
        result = {
            'is_malicious': False,
            'feed_updated': None
        }
        
        # Check cache
        cache_key = f'openphish_{hashlib.md5(url.encode()).hexdigest()}'
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if time.time() - cached['timestamp'] < self.cache_ttl:
                return cached['data']
        
        try:
            # OpenPhish provides a feed of phishing URLs
            feed_url = 'https://openphish.com/feed.txt'
            
            # Download feed (in production, cache this feed)
            response = requests.get(feed_url, timeout=15)
            
            if response.status_code == 200:
                phishing_urls = response.text.strip().split('\n')
                
                # Normalize URL for comparison
                url_normalized = url.rstrip('/')
                
                if url_normalized in phishing_urls or url in phishing_urls:
                    result['is_malicious'] = True
                    result['feed_updated'] = datetime.now().isoformat()
            
            # Cache result
            self.cache[cache_key] = {
                'timestamp': time.time(),
                'data': result
            }
            
        except Exception as e:
            pass
        
        return result
    
    def clear_cache(self):
        """Clear the threat intelligence cache."""
        self.cache = {}

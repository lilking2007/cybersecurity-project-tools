"""
Feature Extraction Engine

Extracts lexical, host-based, network, and content features from URLs.
"""

import re
import math
from typing import Dict, List
from urllib.parse import urlparse
import tldextract


class LexicalFeatureExtractor:
    """Extract lexical features from URLs."""
    
    def extract(self, url: str, parsed_data: Dict) -> Dict[str, any]:
        """
        Extract lexical features from URL.
        
        Args:
            url: Original URL string
            parsed_data: Parsed URL components from URLPreprocessor
            
        Returns:
            Dictionary of lexical features
        """
        features = {}
        
        # Basic length features
        features['url_length'] = len(url)
        features['hostname_length'] = len(parsed_data['hostname']) if parsed_data['hostname'] else 0
        features['path_length'] = len(parsed_data['path'])
        features['query_length'] = len(parsed_data['query'])
        
        # Domain features
        features['domain_length'] = len(parsed_data['domain']) if parsed_data['domain'] else 0
        features['subdomain_length'] = len(parsed_data['subdomain']) if parsed_data['subdomain'] else 0
        
        # Count features
        features['dot_count'] = url.count('.')
        features['hyphen_count'] = url.count('-')
        features['underscore_count'] = url.count('_')
        features['slash_count'] = url.count('/')
        features['question_count'] = url.count('?')
        features['equal_count'] = url.count('=')
        features['at_count'] = url.count('@')
        features['ampersand_count'] = url.count('&')
        features['exclamation_count'] = url.count('!')
        features['tilde_count'] = url.count('~')
        features['percent_count'] = url.count('%')
        features['hash_count'] = url.count('#')
        
        # Digit and letter counts
        features['digit_count'] = sum(c.isdigit() for c in url)
        features['letter_count'] = sum(c.isalpha() for c in url)
        
        # Ratios
        url_len = len(url) if len(url) > 0 else 1
        features['digit_ratio'] = features['digit_count'] / url_len
        features['letter_ratio'] = features['letter_count'] / url_len
        
        # Path features
        path_tokens = [t for t in parsed_data['path'].split('/') if t]
        features['path_token_count'] = len(path_tokens)
        features['avg_path_token_length'] = sum(len(t) for t in path_tokens) / len(path_tokens) if path_tokens else 0
        
        # Query parameter features
        features['query_param_count'] = len(parsed_data['query_params'])
        
        # Subdomain features
        subdomain_tokens = parsed_data['subdomain'].split('.') if parsed_data['subdomain'] else []
        features['subdomain_token_count'] = len(subdomain_tokens)
        
        # Entropy (measure of randomness)
        features['url_entropy'] = self._calculate_entropy(url)
        features['hostname_entropy'] = self._calculate_entropy(parsed_data['hostname']) if parsed_data['hostname'] else 0
        
        # Boolean features
        features['has_port'] = parsed_data['port'] is not None
        features['has_fragment'] = len(parsed_data['fragment']) > 0
        features['is_https'] = parsed_data['scheme'] == 'https'
        
        # Consecutive character patterns
        features['max_consecutive_digits'] = self._max_consecutive_chars(url, str.isdigit)
        features['max_consecutive_letters'] = self._max_consecutive_chars(url, str.isalpha)
        
        return features
    
    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text."""
        if not text:
            return 0.0
        
        # Count character frequencies
        char_freq = {}
        for char in text:
            char_freq[char] = char_freq.get(char, 0) + 1
        
        # Calculate entropy
        entropy = 0.0
        text_len = len(text)
        for count in char_freq.values():
            probability = count / text_len
            entropy -= probability * math.log2(probability)
        
        return entropy
    
    def _max_consecutive_chars(self, text: str, condition) -> int:
        """Find maximum consecutive characters matching a condition."""
        max_count = 0
        current_count = 0
        
        for char in text:
            if condition(char):
                current_count += 1
                max_count = max(max_count, current_count)
            else:
                current_count = 0
        
        return max_count


class SuspiciousPatternExtractor:
    """Extract suspicious pattern features."""
    
    def __init__(self):
        """Initialize with pattern lists."""
        self.brand_keywords = [
            'paypal', 'amazon', 'microsoft', 'google', 'apple', 'facebook',
            'netflix', 'instagram', 'twitter', 'linkedin', 'ebay', 'alibaba',
            'bank', 'chase', 'wellsfargo', 'citibank', 'hsbc'
        ]
        
        self.phishing_keywords = [
            'verify', 'account', 'update', 'confirm', 'login', 'signin',
            'secure', 'suspended', 'locked', 'unusual', 'click', 'here',
            'urgent', 'immediately', 'expire', 'password', 'credential',
            'billing', 'payment', 'refund', 'prize', 'winner'
        ]
    
    def extract(self, url: str, parsed_data: Dict) -> Dict[str, any]:
        """
        Extract suspicious pattern features.
        
        Args:
            url: Original URL
            parsed_data: Parsed URL components
            
        Returns:
            Dictionary of suspicious pattern features
        """
        features = {}
        url_lower = url.lower()
        
        # Brand impersonation detection
        brand_matches = [brand for brand in self.brand_keywords if brand in url_lower]
        features['brand_keyword_count'] = len(brand_matches)
        features['has_brand_keyword'] = len(brand_matches) > 0
        features['brand_keywords'] = brand_matches
        
        # Phishing keyword detection
        phishing_matches = [kw for kw in self.phishing_keywords if kw in url_lower]
        features['phishing_keyword_count'] = len(phishing_matches)
        features['has_phishing_keyword'] = len(phishing_matches) > 0
        features['phishing_keywords'] = phishing_matches
        
        # Combined suspicious score
        features['combined_suspicious_keywords'] = len(set(brand_matches + phishing_matches))
        
        # Typosquatting patterns
        features['has_repeated_chars'] = bool(re.search(r'(.)\1{2,}', url))
        features['has_mixed_case'] = url != url.lower() and url != url.upper()
        
        # Obfuscation techniques
        features['has_hex_encoding'] = bool(re.search(r'%[0-9a-fA-F]{2}', url))
        features['hex_encoding_count'] = len(re.findall(r'%[0-9a-fA-F]{2}', url))
        
        # Suspicious TLD combinations
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work']
        features['has_suspicious_tld'] = any(url_lower.endswith(tld) for tld in suspicious_tlds)
        
        # Double extensions (e.g., .pdf.exe)
        features['has_double_extension'] = bool(re.search(r'\.[a-z]{2,4}\.[a-z]{2,4}$', url_lower))
        
        # Homograph attack indicators
        features['has_non_ascii'] = not url.isascii()
        features['non_ascii_count'] = sum(1 for c in url if ord(c) > 127)
        
        return features


class FeatureExtractor:
    """Main feature extraction coordinator."""
    
    def __init__(self):
        """Initialize feature extractors."""
        self.lexical_extractor = LexicalFeatureExtractor()
        self.pattern_extractor = SuspiciousPatternExtractor()
    
    def extract_all(self, url: str, parsed_data: Dict) -> Dict[str, any]:
        """
        Extract all features from URL.
        
        Args:
            url: Original URL
            parsed_data: Parsed URL components
            
        Returns:
            Dictionary containing all extracted features
        """
        features = {}
        
        # Extract lexical features
        lexical_features = self.lexical_extractor.extract(url, parsed_data)
        features.update({f'lexical_{k}': v for k, v in lexical_features.items()})
        
        # Extract suspicious patterns
        pattern_features = self.pattern_extractor.extract(url, parsed_data)
        features.update({f'pattern_{k}': v for k, v in pattern_features.items()})
        
        return features

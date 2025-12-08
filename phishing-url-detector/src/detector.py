"""
Phishing Detection Engine

Main orchestrator that coordinates all components for URL analysis.
"""

from typing import Dict, List
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from preprocessing.url_parser import URLPreprocessor
from features.lexical_features import FeatureExtractor
from features.host_features import HostBasedFeatureExtractor
from features.network_features import NetworkFeatureExtractor
from models.classifier import PhishingClassifier
from threat_intel.checker import ThreatIntelligenceChecker
from utils.config_loader import get_config


class PhishingDetector:
    """Main phishing detection engine."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize phishing detector.
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = get_config(config_path)
        
        # Initialize components
        self.url_preprocessor = URLPreprocessor(
            max_length=self.config.get('security.max_url_length', 2048)
        )
        
        self.feature_extractor = FeatureExtractor()
        
        self.host_extractor = HostBasedFeatureExtractor(
            whois_timeout=self.config.get('features.host_based.whois_timeout', 5),
            dns_timeout=self.config.get('features.host_based.dns_timeout', 3)
        )
        
        self.network_extractor = NetworkFeatureExtractor(
            request_timeout=self.config.get('features.network.request_timeout', 10),
            max_redirects=self.config.get('features.network.max_redirects', 5)
        )
        
        self.threat_intel = ThreatIntelligenceChecker(
            config=self.config.get_all()
        )
        
        # Initialize ML classifier
        model_type = self.config.get('model.type', 'ensemble')
        self.classifier = PhishingClassifier(model_type=model_type)
        
        # Load pre-trained model if exists
        model_path = self.config.get('model.path')
        if model_path and Path(model_path).exists():
            try:
                self.classifier.load(model_path)
            except Exception as e:
                print(f"Warning: Could not load model from {model_path}: {e}")
    
    def analyze_url(self, url: str, include_network: bool = True) -> Dict:
        """
        Analyze a URL for phishing indicators.
        
        Args:
            url: URL to analyze
            include_network: Whether to include network-based features (slower)
            
        Returns:
            Dictionary containing analysis results
        """
        result = {
            'url': url,
            'is_phishing': False,
            'risk_score': 0.0,
            'risk_level': 'SAFE',
            'confidence': 0.0,
            'features': {},
            'reasons': [],
            'threat_intel_matches': [],
            'analysis_details': {}
        }
        
        try:
            # Step 1: Preprocess and parse URL
            parsed_data = self.url_preprocessor.parse(url)
            suspicious_patterns = self.url_preprocessor.extract_suspicious_patterns(url)
            
            # Step 2: Extract features
            all_features = {}
            
            # Lexical features
            lexical_features = self.feature_extractor.extract_all(url, parsed_data)
            all_features.update(lexical_features)
            
            # Host-based features (if enabled)
            if self.config.get('features.host_based.enabled', True):
                host_features = self.host_extractor.extract(parsed_data)
                all_features.update({f'host_{k}': v for k, v in host_features.items()})
            
            # Network features (if enabled and requested)
            if include_network and self.config.get('features.network.enabled', True):
                network_features = self.network_extractor.extract(url, parsed_data)
                all_features.update({f'network_{k}': v for k, v in network_features.items()})
            
            result['features'] = all_features
            
            # Step 3: Check threat intelligence
            threat_intel_result = self.threat_intel.check_all(url)
            result['threat_intel_matches'] = threat_intel_result['threat_sources']
            result['analysis_details']['threat_intel'] = threat_intel_result
            
            # If found in threat intel, mark as high risk
            if threat_intel_result['is_malicious']:
                result['is_phishing'] = True
                result['risk_score'] = 0.95
                result['risk_level'] = 'HIGH'
                result['confidence'] = 0.95
                result['reasons'].append(
                    f"URL found in threat intelligence databases: {', '.join(threat_intel_result['threat_sources'])}"
                )
                return result
            
            # Step 4: ML Classification
            if self.classifier.is_trained:
                prediction, confidence = self.classifier.predict(all_features)
                
                result['is_phishing'] = bool(prediction)
                result['confidence'] = confidence
                result['risk_score'] = confidence
                result['risk_level'] = self.classifier.get_risk_level(confidence)
                
                # Generate reasons based on features
                reasons = self._generate_reasons(all_features, suspicious_patterns, parsed_data)
                result['reasons'] = reasons
            else:
                # Fallback to rule-based detection
                rule_result = self._rule_based_detection(all_features, suspicious_patterns)
                result.update(rule_result)
            
        except Exception as e:
            result['error'] = str(e)
            result['risk_level'] = 'UNKNOWN'
        
        return result
    
    def _generate_reasons(self, features: Dict, suspicious_patterns: Dict, parsed_data: Dict) -> List[str]:
        """Generate human-readable reasons for the classification."""
        reasons = []
        
        # Check domain age
        domain_age = features.get('host_whois_domain_age_days', -1)
        if 0 <= domain_age < 7:
            reasons.append(f"Domain registered very recently ({domain_age} days ago)")
        elif 0 <= domain_age < 30:
            reasons.append(f"Domain is less than a month old ({domain_age} days)")
        
        # Check SSL
        if not features.get('host_ssl_valid', False) and parsed_data.get('scheme') == 'https':
            reasons.append("Invalid or missing SSL certificate")
        
        # Check suspicious keywords
        if suspicious_patterns.get('suspicious_keyword_count', 0) > 0:
            keywords = suspicious_patterns.get('suspicious_keywords', [])
            reasons.append(f"Contains suspicious keywords: {', '.join(keywords[:3])}")
        
        # Check IP address
        if suspicious_patterns.get('is_ip_address'):
            reasons.append("Uses IP address instead of domain name")
        
        # Check URL length
        if features.get('lexical_url_length', 0) > 100:
            reasons.append("Unusually long URL")
        
        # Check excessive subdomains
        if suspicious_patterns.get('subdomain_count', 0) > 3:
            reasons.append(f"Excessive subdomains ({suspicious_patterns['subdomain_count']})")
        
        # Check for @ symbol
        if suspicious_patterns.get('has_at_symbol'):
            reasons.append("Contains @ symbol (potential credential phishing)")
        
        # Check entropy
        if features.get('lexical_url_entropy', 0) > 4.5:
            reasons.append("High URL randomness (possible obfuscation)")
        
        # Check redirects
        if features.get('network_redirect_to_different_domain'):
            reasons.append("Redirects to a different domain")
        
        return reasons
    
    def _rule_based_detection(self, features: Dict, suspicious_patterns: Dict) -> Dict:
        """Fallback rule-based detection when ML model is not available."""
        risk_score = 0.0
        reasons = []
        
        # Domain age check
        domain_age = features.get('host_whois_domain_age_days', -1)
        if 0 <= domain_age < 7:
            risk_score += 0.3
            reasons.append(f"Very new domain ({domain_age} days)")
        
        # SSL check
        if not features.get('host_ssl_valid', False):
            risk_score += 0.2
            reasons.append("No valid SSL certificate")
        
        # Suspicious keywords
        keyword_count = suspicious_patterns.get('suspicious_keyword_count', 0)
        if keyword_count > 0:
            risk_score += min(0.3, keyword_count * 0.1)
            reasons.append(f"Contains {keyword_count} suspicious keywords")
        
        # IP address
        if suspicious_patterns.get('is_ip_address'):
            risk_score += 0.4
            reasons.append("Uses IP address")
        
        # URL length
        if features.get('lexical_url_length', 0) > 100:
            risk_score += 0.1
            reasons.append("Unusually long URL")
        
        # Cap at 1.0
        risk_score = min(1.0, risk_score)
        
        return {
            'is_phishing': risk_score >= 0.5,
            'risk_score': risk_score,
            'risk_level': self._get_risk_level_from_score(risk_score),
            'confidence': risk_score,
            'reasons': reasons
        }
    
    def _get_risk_level_from_score(self, score: float) -> str:
        """Convert risk score to level."""
        if score >= 0.7:
            return "HIGH"
        elif score >= 0.4:
            return "MEDIUM"
        elif score >= 0.2:
            return "LOW"
        else:
            return "SAFE"

"""
Utility functions for the phishing detector.
"""

import hashlib
import json
from datetime import datetime
from typing import Any, Dict


def hash_url(url: str) -> str:
    """
    Create a hash of a URL for caching/indexing.
    
    Args:
        url: URL to hash
        
    Returns:
        MD5 hash of the URL
    """
    return hashlib.md5(url.encode()).hexdigest()


def format_timestamp(dt: datetime = None) -> str:
    """
    Format datetime as ISO string.
    
    Args:
        dt: Datetime object (default: now)
        
    Returns:
        ISO formatted timestamp
    """
    if dt is None:
        dt = datetime.now()
    return dt.isoformat()


def sanitize_url_for_display(url: str, max_length: int = 100) -> str:
    """
    Sanitize URL for safe display.
    
    Args:
        url: URL to sanitize
        max_length: Maximum display length
        
    Returns:
        Sanitized URL string
    """
    if len(url) > max_length:
        return url[:max_length] + '...'
    return url


def calculate_risk_color(risk_score: float) -> str:
    """
    Get color code for risk score.
    
    Args:
        risk_score: Risk score (0-1)
        
    Returns:
        Color code string
    """
    if risk_score >= 0.7:
        return '#ef4444'  # Red
    elif risk_score >= 0.4:
        return '#f59e0b'  # Orange
    elif risk_score >= 0.2:
        return '#eab308'  # Yellow
    else:
        return '#10b981'  # Green


def export_results_json(results: Dict, filepath: str):
    """
    Export analysis results to JSON file.
    
    Args:
        results: Analysis results dictionary
        filepath: Output file path
    """
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)


def load_results_json(filepath: str) -> Dict:
    """
    Load analysis results from JSON file.
    
    Args:
        filepath: Input file path
        
    Returns:
        Results dictionary
    """
    with open(filepath, 'r') as f:
        return json.load(f)

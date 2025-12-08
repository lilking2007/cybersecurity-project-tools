"""
Flask Web Application for Phishing URL Detector

Provides REST API and web dashboard for phishing detection.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sys
from pathlib import Path
import logging
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from detector import PhishingDetector
from utils.config_loader import get_config

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load configuration
config = get_config()
app.config['SECRET_KEY'] = config.get('app.secret_key', 'change-this-secret-key')

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[config.get('api.rate_limit', '100/minute')]
)

# Initialize detector
detector = PhishingDetector()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """Render main dashboard."""
    return render_template('index.html')


@app.route('/api/v1/check', methods=['POST'])
@limiter.limit("50/minute")
def check_url():
    """
    Check a URL for phishing indicators.
    
    Request JSON:
    {
        "url": "https://example.com",
        "include_network": true  // optional, default true
    }
    
    Response JSON:
    {
        "url": "https://example.com",
        "is_phishing": false,
        "risk_score": 0.23,
        "risk_level": "LOW",
        "confidence": 0.23,
        "reasons": [...],
        "threat_intel_matches": [],
        "timestamp": "2024-01-01T12:00:00"
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'Missing required field: url'
            }), 400
        
        url = data['url']
        include_network = data.get('include_network', True)
        
        # Analyze URL
        logger.info(f"Analyzing URL: {url}")
        result = detector.analyze_url(url, include_network=include_network)
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        
        # Log result
        logger.info(f"Analysis complete: {url} - Risk: {result['risk_level']}")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error analyzing URL: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/v1/batch', methods=['POST'])
@limiter.limit("10/minute")
def check_batch():
    """
    Check multiple URLs in batch.
    
    Request JSON:
    {
        "urls": ["https://example1.com", "https://example2.com"],
        "include_network": false  // optional
    }
    
    Response JSON:
    {
        "results": [
            {
                "url": "https://example1.com",
                "is_phishing": false,
                ...
            },
            ...
        ],
        "total": 2,
        "phishing_count": 0
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'urls' not in data:
            return jsonify({
                'error': 'Missing required field: urls'
            }), 400
        
        urls = data['urls']
        include_network = data.get('include_network', False)  # Faster for batch
        
        if not isinstance(urls, list):
            return jsonify({
                'error': 'urls must be a list'
            }), 400
        
        if len(urls) > 50:
            return jsonify({
                'error': 'Maximum 50 URLs per batch request'
            }), 400
        
        # Analyze all URLs
        results = []
        phishing_count = 0
        
        for url in urls:
            result = detector.analyze_url(url, include_network=include_network)
            result['timestamp'] = datetime.now().isoformat()
            results.append(result)
            
            if result['is_phishing']:
                phishing_count += 1
        
        return jsonify({
            'results': results,
            'total': len(results),
            'phishing_count': phishing_count
        }), 200
        
    except Exception as e:
        logger.error(f"Error in batch analysis: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': detector.classifier.is_trained,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """Get system statistics."""
    # In production, this would query a database
    return jsonify({
        'total_checks': 0,
        'phishing_detected': 0,
        'model_accuracy': 0.0,
        'uptime_seconds': 0
    }), 200


@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded."""
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description)
    }), 429


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    # Get configuration
    host = config.get('app.host', '0.0.0.0')
    port = config.get('app.port', 5000)
    debug = config.get('app.debug', False)
    
    logger.info(f"Starting Phishing URL Detector on {host}:{port}")
    logger.info(f"Model loaded: {detector.classifier.is_trained}")
    
    app.run(host=host, port=port, debug=debug)

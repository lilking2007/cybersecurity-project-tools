# Phishing Website Detector

A comprehensive ML-based phishing URL detection system with real-time threat analysis, threat intelligence integration, and a web dashboard.

## 🎯 Features

- **Real-time URL Analysis** - Instant phishing detection with confidence scoring
- **ML Classification** - Ensemble models (Random Forest, XGBoost, Logistic Regression)
- **Multi-layer Feature Extraction** - Lexical, host-based, network, and content features
- **Threat Intelligence Integration** - PhishTank, OpenPhish, VirusTotal, URLhaus
- **Web Dashboard** - Flask-based UI with admin monitoring
- **REST API** - Easy integration with other tools
- **Alerting System** - Email, Slack, webhooks for high-risk URLs
- **Analytics** - Real-time metrics and threat trends

## 🏗️ Architecture

```
┌─────────────────┐
│  URL Ingestion  │ ← User Input, API, Browser Extension
└────────┬────────┘
         │
┌────────▼────────┐
│  Preprocessing  │ ← URL parsing, sanitization
└────────┬────────┘
         │
┌────────▼────────┐
│Feature Extraction│ ← Lexical, Host, Network, Content
└────────┬────────┘
         │
┌────────▼────────┐
│ ML Classification│ ← Ensemble models, threat intel
└────────┬────────┘
         │
┌────────▼────────┐
│ Risk Scoring &  │ ← Confidence, labels, explanations
│    Alerting     │
└────────┬────────┘
         │
┌────────▼────────┐
│  Dashboard/API  │ ← Web UI, REST endpoints
└─────────────────┘
```

## 📁 Project Structure

```
phishing-url-detector/
├── src/
│   ├── preprocessing/       # URL parsing and sanitization
│   ├── features/           # Feature extraction modules
│   ├── models/             # ML models and training
│   ├── threat_intel/       # External API integrations
│   ├── alerting/           # Notification system
│   └── utils/              # Helper functions
├── app/
│   ├── api/                # Flask REST API
│   ├── dashboard/          # Web UI
│   └── static/             # CSS, JS, images
├── data/
│   ├── raw/                # Raw phishing/benign URLs
│   ├── processed/          # Processed features
│   └── models/             # Trained model artifacts
├── config/                 # Configuration files
├── tests/                  # Unit and integration tests
├── docker/                 # Docker configuration
└── docs/                   # Documentation

```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Redis (for task queuing)
- Docker (optional, for containerized deployment)

### Installation

```bash
# Clone the repository
cd phishing-url-detector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your API keys

# Initialize database
python scripts/init_db.py

# Train initial model (or download pre-trained)
python scripts/train_model.py
```

### Running the Application

```bash
# Start Redis (in separate terminal)
redis-server

# Start Flask application
python app/main.py

# Access dashboard at http://localhost:5000
```

### Using the API

```bash
# Check a URL
curl -X POST http://localhost:5000/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example-suspicious-site.com"}'

# Response
{
  "url": "https://example-suspicious-site.com",
  "risk_score": 0.87,
  "risk_level": "HIGH",
  "confidence": 0.92,
  "features": {
    "domain_age_days": 3,
    "has_ssl": false,
    "suspicious_keywords": true
  },
  "reasons": [
    "Domain registered less than 7 days ago",
    "No valid SSL certificate",
    "Contains suspicious keywords: 'verify-account'"
  ],
  "threat_intel_matches": ["PhishTank", "URLhaus"]
}
```

## 🔧 Configuration

Edit `config/config.yaml`:

```yaml
# API Keys
phishtank_api_key: "your-key-here"
virustotal_api_key: "your-key-here"

# Model settings
model:
  type: "ensemble"
  threshold: 0.7

# Alerting
alerts:
  email:
    enabled: true
    smtp_server: "smtp.gmail.com"
  slack:
    enabled: true
    webhook_url: "your-webhook-url"
```

## 📊 Data Sources

- **PhishTank** - Community-verified phishing URLs
- **OpenPhish** - Real-time phishing feed
- **URLhaus** - Malware URL database
- **Google Safe Browsing** - URL reputation
- **VirusTotal** - Multi-engine URL scanning

## 🤖 Machine Learning

### Models Used
- Logistic Regression (baseline)
- Random Forest Classifier
- XGBoost Gradient Boosting
- Ensemble Voting Classifier

### Features Extracted (50+ features)
- **Lexical**: URL length, special characters, suspicious patterns
- **Host-based**: Domain age, WHOIS data, SSL certificates
- **Network**: DNS records, IP geolocation, redirects
- **Content**: HTML analysis, form detection, brand impersonation

### Training

```bash
# Train with default settings
python scripts/train_model.py

# Train with custom dataset
python scripts/train_model.py --data data/custom_dataset.csv

# Evaluate model
python scripts/evaluate_model.py
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Services will be available at:
# - Web UI: http://localhost:5000
# - API: http://localhost:5000/api/v1
# - Redis: localhost:6379
```

## 📈 Monitoring & Analytics

Access the admin dashboard at `/admin` to view:
- Detection accuracy metrics
- False positive/negative rates
- Most targeted brands
- URL submission trends
- Threat intelligence matches

## 🔒 Security Features

- API rate limiting (100 requests/minute)
- URL sanitization and validation
- JWT authentication for API access
- Audit logging for all submissions
- Sandboxed content analysis

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test suite
pytest tests/test_features.py
```

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## 📧 Contact

For questions or support, please open an issue on GitHub.

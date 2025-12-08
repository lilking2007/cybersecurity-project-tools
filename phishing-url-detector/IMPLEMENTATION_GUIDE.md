# Phishing URL Detector - Implementation Guide

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [API Reference](#api-reference)
7. [Training Custom Models](#training-custom-models)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

## Overview

The Phishing URL Detector is a comprehensive machine learning-based system for detecting phishing websites. It combines:

- **Multi-layer Feature Extraction**: Lexical, host-based, network, and content features
- **Ensemble ML Models**: Random Forest, XGBoost, and Logistic Regression
- **Threat Intelligence Integration**: PhishTank, URLhaus, OpenPhish, VirusTotal
- **Real-time Analysis**: Fast URL scanning with confidence scoring
- **Web Dashboard**: Modern, responsive UI for easy interaction
- **REST API**: Easy integration with other security tools

## Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Flask Web Application                    │
│                    (app/main.py)                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  Phishing Detector Engine                    │
│                    (src/detector.py)                         │
└─┬────────┬────────┬────────┬────────┬────────────────────────┘
  │        │        │        │        │
  ▼        ▼        ▼        ▼        ▼
┌───┐   ┌───┐   ┌───┐   ┌───┐   ┌────────┐
│URL│   │Lex│   │Host│  │Net│   │Threat  │
│Pre│   │Feat│   │Feat│  │Feat│  │Intel   │
└───┘   └───┘   └───┘   └───┘   └────────┘
                                      │
                       ┌──────────────┴──────────────┐
                       ▼                             ▼
                  ┌─────────┐                  ┌─────────┐
                  │ML Model │                  │External │
                  │Ensemble │                  │APIs     │
                  └─────────┘                  └─────────┘
```

### Data Flow

1. **URL Ingestion**: User submits URL via web UI or API
2. **Preprocessing**: URL is parsed, validated, and sanitized
3. **Feature Extraction**: 50+ features extracted across multiple categories
4. **Threat Intel Check**: URL checked against known phishing databases
5. **ML Classification**: Ensemble model predicts phishing probability
6. **Risk Scoring**: Confidence score and risk level calculated
7. **Response**: Results returned with explanations

## Installation

### Method 1: Quick Start (Recommended)

```bash
# Navigate to project directory
cd phishing-url-detector

# Run quick start script
python quick_start.py
```

The script will:
- Check Python version (3.9+ required)
- Create necessary directories
- Install dependencies
- Set up configuration
- Train initial model
- Start the application

### Method 2: Manual Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p data/models data/raw data/processed logs

# Copy configuration
copy .env.example .env

# Train model
python scripts/train_model.py

# Start application
python app/main.py
```

### Method 3: Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:5000
```

## Configuration

### Environment Variables

Edit `.env` file:

```bash
# Flask
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=false

# Threat Intelligence API Keys
PHISHTANK_API_KEY=your-phishtank-key
VIRUSTOTAL_API_KEY=your-virustotal-key
GOOGLE_SAFE_BROWSING_API_KEY=your-google-key

# Email Alerts (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Configuration File

Edit `config/config.yaml`:

```yaml
model:
  type: ensemble  # Options: logistic, random_forest, xgboost, ensemble
  threshold: 0.7

features:
  lexical:
    enabled: true
  host_based:
    enabled: true
  network:
    enabled: true  # Set to false for faster analysis
```

## Usage

### Web Dashboard

1. Start the application:
   ```bash
   python app/main.py
   ```

2. Open browser to `http://localhost:5000`

3. Enter URL and click "Analyze URL"

4. View results:
   - Risk level (SAFE, LOW, MEDIUM, HIGH)
   - Confidence score
   - Detection reasons
   - Threat intelligence matches

### REST API

#### Check Single URL

```bash
curl -X POST http://localhost:5000/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://suspicious-site.com",
    "include_network": true
  }'
```

Response:
```json
{
  "url": "https://suspicious-site.com",
  "is_phishing": true,
  "risk_score": 0.87,
  "risk_level": "HIGH",
  "confidence": 0.92,
  "reasons": [
    "Domain registered less than 7 days ago",
    "No valid SSL certificate",
    "Contains suspicious keywords: verify, account"
  ],
  "threat_intel_matches": ["PhishTank", "URLhaus"],
  "timestamp": "2024-01-01T12:00:00"
}
```

#### Batch Check

```bash
curl -X POST http://localhost:5000/api/v1/batch \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://example1.com",
      "https://example2.com"
    ],
    "include_network": false
  }'
```

### Python SDK

```python
from src.detector import PhishingDetector

# Initialize detector
detector = PhishingDetector()

# Analyze URL
result = detector.analyze_url("https://suspicious-site.com")

print(f"Risk Level: {result['risk_level']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Reasons: {result['reasons']}")
```

## API Reference

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web dashboard |
| `/api/v1/check` | POST | Check single URL |
| `/api/v1/batch` | POST | Check multiple URLs |
| `/api/v1/health` | GET | Health check |
| `/api/v1/stats` | GET | System statistics |

### Rate Limits

- `/api/v1/check`: 50 requests/minute
- `/api/v1/batch`: 10 requests/minute
- Default: 100 requests/minute

## Training Custom Models

### Prepare Dataset

Create CSV file with columns:
- `url`: The URL string
- `label`: 0 for benign, 1 for phishing

Example:
```csv
url,label
https://www.google.com,0
http://paypal-verify.tk/login,1
https://www.github.com,0
http://secure-banking.ml/update,1
```

### Train Model

```bash
# Train with custom dataset
python scripts/train_model.py --data path/to/dataset.csv --output data/models/custom_model.pkl

# Update config to use new model
# Edit config/config.yaml:
# model:
#   path: data/models/custom_model.pkl
```

### Data Sources

Recommended sources for training data:

1. **PhishTank**: https://www.phishtank.com/developer_info.php
2. **OpenPhish**: https://openphish.com/
3. **URLhaus**: https://urlhaus.abuse.ch/
4. **Alexa Top Sites**: For benign URLs
5. **Common Crawl**: For benign URLs

## Deployment

### Production Checklist

- [ ] Set `FLASK_DEBUG=false` in `.env`
- [ ] Use strong `FLASK_SECRET_KEY`
- [ ] Configure API keys for threat intelligence
- [ ] Set up HTTPS with SSL certificate
- [ ] Configure rate limiting
- [ ] Set up monitoring and logging
- [ ] Configure backup for model and data
- [ ] Set up alerting (email/Slack)

### Docker Deployment

```bash
# Build image
docker build -f docker/Dockerfile -t phishing-detector .

# Run container
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/config:/app/config \
  --name phishing-detector \
  phishing-detector
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name phishing-detector.example.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

### Common Issues

#### 1. Model Not Loading

**Problem**: "Model not trained" error

**Solution**:
```bash
# Train a new model
python scripts/train_model.py

# Or download pre-trained model
# Place in data/models/phishing_model.pkl
```

#### 2. WHOIS Timeout

**Problem**: WHOIS queries timing out

**Solution**: Increase timeout in `config/config.yaml`:
```yaml
features:
  host_based:
    whois_timeout: 10  # Increase from 5
```

#### 3. SSL Certificate Errors

**Problem**: SSL verification errors

**Solution**: Network features use `verify=False` for analysis purposes. This is intentional for detecting invalid certificates.

#### 4. Rate Limit Exceeded

**Problem**: 429 Too Many Requests

**Solution**: Adjust rate limits in `config/config.yaml`:
```yaml
api:
  rate_limit: "200/minute"  # Increase limit
```

### Performance Optimization

1. **Disable Network Features** for faster analysis:
   ```yaml
   features:
     network:
       enabled: false
   ```

2. **Use Batch API** for multiple URLs

3. **Enable Caching** for threat intelligence

4. **Use Redis** for distributed caching

### Logging

View logs:
```bash
# Application logs
tail -f logs/phishing_detector.log

# Audit logs
tail -f logs/audit.log
```

## Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Documentation: See README.md
- Email: security-team@example.com

## License

MIT License - See LICENSE file for details

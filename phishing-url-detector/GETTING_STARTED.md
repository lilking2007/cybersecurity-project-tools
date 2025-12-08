# 🚀 Getting Started with Phishing URL Detector

Welcome! This guide will help you get the Phishing URL Detector up and running in minutes.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.9 or higher** installed
- **pip** package manager
- **Git** (optional, for version control)
- **Redis** (optional, for production deployment)

Check your Python version:
```bash
python --version
```

## 🎯 Quick Start (5 Minutes)

### Step 1: Navigate to Project Directory

```bash
cd "c:\Users\kipch\Documents\2. Projects\Cybersecurity project tools\phishing-url-detector"
```

### Step 2: Run the Quick Start Script

```bash
python quick_start.py
```

The script will guide you through:
1. ✅ Checking Python version
2. ✅ Creating necessary directories
3. ✅ Installing dependencies
4. ✅ Setting up configuration
5. ✅ Training initial model
6. ✅ Starting the application

### Step 3: Access the Dashboard

Open your browser to:
```
http://localhost:5000
```

**That's it! You're ready to analyze URLs!** 🎉

## 🔧 Manual Installation (Alternative)

If you prefer manual setup:

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create Directories

```bash
# Windows PowerShell:
New-Item -ItemType Directory -Force -Path data\models, data\raw, data\processed, logs

# Linux/Mac:
mkdir -p data/models data/raw data/processed logs
```

### 4. Configure Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env and add your API keys (optional)
notepad .env
```

### 5. Train Initial Model

```bash
python scripts/train_model.py
```

### 6. Start the Application

```bash
python app/main.py
```

## 🌐 Using the Web Dashboard

### Analyze a URL

1. **Enter URL**: Type or paste a URL in the input field
   ```
   Example: https://suspicious-site.com
   ```

2. **Click Analyze**: Press the "🔍 Analyze URL" button

3. **View Results**:
   - **Risk Level**: SAFE, LOW, MEDIUM, or HIGH
   - **Risk Score**: Percentage (0-100%)
   - **Confidence**: How confident the model is
   - **Reasons**: Why the URL was flagged
   - **Threat Intel**: External database matches

### Understanding Results

| Risk Level | Score Range | Meaning |
|------------|-------------|---------|
| 🟢 SAFE | 0-30% | URL appears legitimate |
| 🟡 LOW | 30-50% | Minor suspicious indicators |
| 🟠 MEDIUM | 50-80% | Multiple suspicious indicators |
| 🔴 HIGH | 80-100% | Strong phishing indicators |

## 💻 Using the CLI Tool

### Check Single URL

```bash
python cli.py https://example.com
```

### Check Multiple URLs from File

```bash
# Create a file with URLs (one per line)
python cli.py --file sample_urls.txt
```

### Fast Analysis (Skip Network Features)

```bash
python cli.py --no-network https://example.com
```

### JSON Output

```bash
python cli.py --json https://example.com
```

## 🔌 Using the REST API

### Check Single URL

```bash
curl -X POST http://localhost:5000/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Check Multiple URLs (Batch)

```bash
curl -X POST http://localhost:5000/api/v1/batch \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://example1.com",
      "https://example2.com"
    ]
  }'
```

### Health Check

```bash
curl http://localhost:5000/api/v1/health
```

## 🐍 Using Python SDK

```python
from src.detector import PhishingDetector

# Initialize detector
detector = PhishingDetector()

# Analyze URL
result = detector.analyze_url("https://suspicious-site.com")

# Print results
print(f"Risk Level: {result['risk_level']}")
print(f"Is Phishing: {result['is_phishing']}")
print(f"Confidence: {result['confidence']:.2%}")

# Check reasons
for reason in result['reasons']:
    print(f"  - {reason}")
```

## 🎓 Training with Your Own Data

### Prepare Dataset

Create a CSV file with two columns:

```csv
url,label
https://www.google.com,0
http://paypal-verify.tk/login,1
https://www.github.com,0
http://secure-banking.ml/update,1
```

- **url**: The URL string
- **label**: 0 = benign, 1 = phishing

### Train Model

```bash
python scripts/train_model.py --data path/to/your_dataset.csv
```

### View Training Results

The script will display:
- Accuracy, Precision, Recall, F1 Score
- Cross-validation scores
- Top 10 most important features

## 🔑 API Keys (Optional but Recommended)

For enhanced detection, configure threat intelligence APIs:

### 1. PhishTank

1. Register at https://www.phishtank.com/api_register.php
2. Get your API key
3. Add to `.env`:
   ```
   PHISHTANK_API_KEY=your-key-here
   ```

### 2. VirusTotal

1. Register at https://www.virustotal.com/
2. Get your API key
3. Add to `.env`:
   ```
   VIRUSTOTAL_API_KEY=your-key-here
   ```

### 3. Google Safe Browsing

1. Create project in Google Cloud Console
2. Enable Safe Browsing API
3. Get API key
4. Add to `.env`:
   ```
   GOOGLE_SAFE_BROWSING_API_KEY=your-key-here
   ```

## 🐳 Docker Deployment

### Quick Start with Docker

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services included:
- **web**: Flask application (port 5000)
- **redis**: Caching and task queue
- **worker**: Background task processor

## 📊 Testing the System

### Test with Sample URLs

```bash
# Use provided sample URLs
python cli.py --file sample_urls.txt
```

### Expected Results

- **Benign URLs** (google.com, github.com): SAFE
- **IP-based URLs**: MEDIUM-HIGH risk
- **Suspicious keywords**: MEDIUM-HIGH risk
- **Suspicious TLDs** (.tk, .ml, .ga): MEDIUM risk

## 🔍 Troubleshooting

### Issue: "Model not trained" error

**Solution**:
```bash
python scripts/train_model.py
```

### Issue: Port 5000 already in use

**Solution**: Change port in `config/config.yaml`:
```yaml
app:
  port: 8080
```

### Issue: Dependencies installation fails

**Solution**:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies one by one
pip install flask scikit-learn xgboost
```

### Issue: WHOIS queries timeout

**Solution**: Increase timeout in `config/config.yaml`:
```yaml
features:
  host_based:
    whois_timeout: 10
```

## 📚 Next Steps

Now that you're up and running:

1. ✅ **Test with sample URLs** - Use `sample_urls.txt`
2. ✅ **Configure API keys** - Enable threat intelligence
3. ✅ **Train with real data** - Use PhishTank/OpenPhish datasets
4. ✅ **Integrate with tools** - Use the REST API
5. ✅ **Deploy to production** - Use Docker or cloud platform

## 📖 Additional Resources

- **README.md** - Project overview and features
- **IMPLEMENTATION_GUIDE.md** - Detailed technical guide
- **PROJECT_SUMMARY.md** - Complete feature list
- **config/config.yaml** - All configuration options

## 💡 Tips for Best Results

1. **Use Real Training Data**: The sample model is for demonstration. Train with 10,000+ labeled URLs for production use.

2. **Enable All Features**: Network features take longer but improve accuracy.

3. **Configure Threat Intelligence**: API integrations significantly improve detection.

4. **Monitor Performance**: Check logs regularly for errors or issues.

5. **Update Regularly**: Retrain models monthly with new phishing campaigns.

## 🎯 Common Use Cases

### Security Operations Center (SOC)
```bash
# Batch check suspicious URLs from incident reports
python cli.py --file incident_urls.txt --json > results.json
```

### Email Security Gateway
```python
# Check URLs from emails
from src.detector import PhishingDetector
detector = PhishingDetector()

for url in email_urls:
    result = detector.analyze_url(url, include_network=False)
    if result['risk_score'] > 0.7:
        quarantine_email()
```

### Browser Extension
```javascript
// Call API from browser extension
fetch('http://localhost:5000/api/v1/check', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({url: currentUrl})
})
```

## 🆘 Getting Help

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Review **IMPLEMENTATION_GUIDE.md**
3. Check application logs in `logs/` directory
4. Create an issue with:
   - Error message
   - Steps to reproduce
   - Your configuration

## ✅ Success Checklist

- [ ] Python 3.9+ installed
- [ ] Dependencies installed
- [ ] Configuration file created
- [ ] Model trained
- [ ] Application running
- [ ] Dashboard accessible
- [ ] Sample URLs tested
- [ ] API keys configured (optional)

---

**Congratulations!** 🎉 You're now ready to detect phishing URLs with machine learning!

For questions or issues, refer to the documentation or create an issue.

**Happy Phishing Hunting!** 🛡️

# Threat Intelligence Platform

A centralized platform for monitoring and analyzing emerging cybersecurity threats through automated data collection, IOC processing, and threat intelligence enrichment.

## Features

- **Multi-Source Data Collection**: Automated ingestion from threat feeds (AbuseIPDB, VirusTotal, Shodan, etc.)
- **IOC Processing**: Parse, normalize, and enrich Indicators of Compromise
- **REST API**: Full-featured API for external integrations
- **Web Dashboard**: Real-time monitoring and analytics interface
- **Automated Enrichment**: Correlation with threat actors, campaigns, and MITRE ATT&CK TTPs
- **Alerting System**: Notifications for high-risk indicators

## Technology Stack

- **Backend**: Django 4.2+ / Django REST Framework
- **Task Queue**: Celery with Redis
- **Database**: SQLite (default) / PostgreSQL (production)
- **APIs**: VirusTotal, Shodan, AbuseIPDB
- **Frontend**: Bootstrap 5, Chart.js

## Quick Start

### Prerequisites

- Python 3.8+
- Redis (for Celery)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd threat-intelligence-platform
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

7. In a separate terminal, start Celery worker:
```bash
celery -A config worker -l info
```

8. (Optional) Start Celery beat for scheduled tasks:
```bash
celery -A config beat -l info
```

## Usage

### Web Dashboard
Access the dashboard at `http://localhost:8000/`

### Admin Interface
Manage IOCs, threat actors, and campaigns at `http://localhost:8000/admin/`

### API Endpoints

- `GET /api/iocs/` - List all IOCs
- `GET /api/iocs/?type=IP` - Filter IOCs by type
- `POST /api/iocs/` - Create new IOC
- `GET /api/actors/` - List threat actors
- `GET /api/campaigns/` - List campaigns

### Manual Feed Ingestion

```python
from data_collection.tasks import ingest_feed
ingest_feed.delay('malware_domains')
```

## Project Structure

```
threat-intelligence-platform/
├── config/              # Django settings and configuration
├── src/
│   ├── core/           # Core models (IOC, ThreatActor, Campaign)
│   ├── data_collection/# Feed parsers and ingestion tasks
│   ├── ioc_processing/ # Enrichment and correlation logic
│   ├── dashboard/      # Web UI views and templates
│   └── api_integration/# REST API and external API clients
├── templates/          # HTML templates
├── static/            # Static files (CSS, JS, images)
└── manage.py          # Django management script
```

## Configuration

### API Keys

Add your API keys to `.env`:
- `VIRUSTOTAL_API_KEY` - VirusTotal API key
- `ABUSEIPDB_API_KEY` - AbuseIPDB API key
- `SHODAN_API_KEY` - Shodan API key

### Adding Custom Feeds

Edit `src/data_collection/feeds.py` to add new threat feeds:

```python
FEEDS = {
    'your_feed_name': TextListFeed('https://example.com/feed.txt'),
}
```

## Deployment

### Production Settings

1. Set `DEBUG=False` in `.env`
2. Configure a production database (PostgreSQL recommended)
3. Set up a reverse proxy (Nginx)
4. Use Gunicorn as WSGI server:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Docker Deployment

(Docker configuration coming soon)

## Security Considerations

- Change `SECRET_KEY` in production
- Enable HTTPS
- Implement rate limiting
- Use environment variables for sensitive data
- Regularly update dependencies

## Contributing

Contributions are welcome! Please submit pull requests or open issues for bugs and feature requests.

## License

MIT License

## Roadmap

- [ ] STIX/TAXII feed support
- [ ] MITRE ATT&CK mapping visualization
- [ ] Elasticsearch integration
- [ ] SIEM/SOAR integrations (TheHive, Cortex)
- [ ] Advanced correlation engine
- [ ] Automated playbook execution
- [ ] Multi-tenancy support

## Support

For issues and questions, please open a GitHub issue.

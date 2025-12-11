from celery import shared_task
from core.models import IOC
from api_integration.clients import VirusTotalClient, AbuseIPDBClient
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def enrich_ioc(ioc_id):
    try:
        ioc = IOC.objects.get(id=ioc_id)
    except IOC.DoesNotExist:
        return

    # Check VirusTotal
    if hasattr(settings, 'VIRUSTOTAL_API_KEY'):
        vt_client = VirusTotalClient(settings.VIRUSTOTAL_API_KEY)
        if ioc.ioc_type == 'IP':
            report = vt_client.get_ip_report(ioc.value)
            if report:
                ioc.virus_total_report = report
                # Update reputation based on malicious votes
                stats = report.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                malicious = stats.get('malicious', 0)
                if malicious > 0:
                    ioc.reputation_score = min(100, malicious * 10) # Simple scoring logic

    # Check AbuseIPDB
    if ioc.ioc_type == 'IP' and hasattr(settings, 'ABUSEIPDB_API_KEY'):
        abuse_client = AbuseIPDBClient(settings.ABUSEIPDB_API_KEY)
        report = abuse_client.check_ip(ioc.value)
        if report:
             data = report.get('data', {})
             score = data.get('abuseConfidenceScore', 0)
             ioc.reputation_score = max(ioc.reputation_score, score)

    ioc.save()
    logger.info(f"Enriched IOC {ioc.value}")

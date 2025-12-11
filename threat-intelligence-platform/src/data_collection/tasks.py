from celery import shared_task
from .feeds import FEEDS
from core.models import IOC
import logging

logger = logging.getLogger(__name__)

@shared_task
def ingest_feed(feed_name):
    if feed_name not in FEEDS:
        logger.error(f"Feed {feed_name} not found")
        return

    feed = FEEDS[feed_name]
    logger.info(f"Starting ingestion for {feed_name}")
    data = feed.fetch_data()
    
    count = 0
    for item in data:
        # Basic type detection (naive)
        ioc_type = 'DOMAIN' # Default for this example
        if item.replace('.', '').isdigit():
             ioc_type = 'IP'
        
        obj, created = IOC.objects.get_or_create(
            value=item,
            defaults={
                'ioc_type': ioc_type,
                'source': feed_name
            }
        )
        if created:
            count += 1
            # Trigger enrichment task here
            from ioc_processing.tasks import enrich_ioc
            enrich_ioc.delay(obj.id)
            
    logger.info(f"Ingested {count} new IOCs from {feed_name}")

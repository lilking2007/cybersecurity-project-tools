from django.core.management.base import BaseCommand
from core.models import IOC, ThreatActor, Campaign, Incident
from django.utils import timezone
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populates the database with sample threat intelligence data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')

        # clear existing data
        IOC.objects.all().delete()
        ThreatActor.objects.all().delete()
        Campaign.objects.all().delete()
        Incident.objects.all().delete()

        # Create Threat Actors
        actors = []
        actor_names = ['APT28', 'Lazarus Group', 'Equation Group', 'DarkSide', 'Cobalt Group']
        for name in actor_names:
            actor = ThreatActor.objects.create(
                name=name,
                description=f"Advanced Persistent Threat group {name}.",
                first_seen=timezone.now() - timedelta(days=random.randint(100, 1000))
            )
            actors.append(actor)

        # Create Campaigns
        campaigns = []
        campaign_names = ['Operation Aurora', 'WannaCry', 'SolarWinds', 'Log4Shell Exploitation', 'Exchange Havoc']
        for name in campaign_names:
            campaign = Campaign.objects.create(
                name=name,
                description=f"Massive exploitation campaign {name}.",
                threat_actor=random.choice(actors)
            )
            campaigns.append(campaign)

        # Create IOCs
        ioc_types = ['IP', 'DOMAIN', 'URL', 'HASH_SHA256']
        sources = ['AbuseIPDB', 'VirusTotal', 'Shodan', 'Internal Honeypot']
        
        for i in range(50):
            ioc_type = random.choice(ioc_types)
            if ioc_type == 'IP':
                value = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
            elif ioc_type == 'DOMAIN':
                value = f"malicious-{random.randint(1000, 9999)}.com"
            elif ioc_type == 'URL':
                value = f"http://phishing-site-{random.randint(100, 999)}.com/login"
            else:
                value = f"a{random.randint(1000000000, 9999999999)}f"
            
            ioc = IOC.objects.create(
                value=value,
                ioc_type=ioc_type,
                source=random.choice(sources),
                reputation_score=random.randint(0, 100),
                created_at=timezone.now() - timedelta(days=random.randint(0, 30))
            )
            if random.random() > 0.7:
                ioc.campaigns.add(random.choice(campaigns))

        # Create Incidents
        incident_titles = ['Unusual Outbound Traffic', 'Suspicious PowerShell Execution', 'Brute Force Attempt', 'Malware Beacon Detected']
        severities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        
        for _ in range(10):
            incident = Incident.objects.create(
                title=random.choice(incident_titles),
                description="Detected anomalous behavior indicating potential compromise.",
                severity=random.choice(severities),
                status='OPEN'
            )
            # Link random IOCs
            incident.iocs.add(*IOC.objects.order_by('?')[:random.randint(1, 3)])

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))

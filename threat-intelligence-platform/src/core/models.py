from django.db import models
from django.utils import timezone

class ThreatActor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    aliases = models.JSONField(default=list, blank=True)
    first_seen = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    threat_actor = models.ForeignKey(ThreatActor, on_delete=models.SET_NULL, null=True, related_name='campaigns')
    
    def __str__(self):
        return self.name

class IOC(models.Model):
    IOC_TYPES = [
        ('IP', 'IP Address'),
        ('DOMAIN', 'Domain'),
        ('URL', 'URL'),
        ('HASH_MD5', 'MD5 Hash'),
        ('HASH_SHA256', 'SHA256 Hash'),
        ('EMAIL', 'Email Address'),
    ]
    
    value = models.CharField(max_length=512, unique=True)
    ioc_type = models.CharField(max_length=20, choices=IOC_TYPES)
    source = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    
    reputation_score = models.IntegerField(default=0) # 0-100 (100 is malicious)
    is_active = models.BooleanField(default=True)
    
    campaigns = models.ManyToManyField(Campaign, blank=True, related_name='iocs')
    
    # Enrichment Data
    geo_country = models.CharField(max_length=50, blank=True, null=True)
    asn = models.CharField(max_length=50, blank=True, null=True)
    whois_data = models.JSONField(default=dict, blank=True)
    virus_total_report = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.ioc_type}: {self.value}"

class Incident(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    iocs = models.ManyToManyField(IOC, related_name='incidents')
    severity = models.CharField(max_length=20, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')])
    status = models.CharField(max_length=20, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

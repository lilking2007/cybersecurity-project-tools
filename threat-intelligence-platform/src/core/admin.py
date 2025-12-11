from django.contrib import admin
from .models import IOC, ThreatActor, Campaign, Incident

@admin.register(IOC)
class IOCAdmin(admin.ModelAdmin):
    list_display = ('value', 'ioc_type', 'reputation_score', 'source', 'created_at', 'is_active')
    list_filter = ('ioc_type', 'is_active', 'source')
    search_fields = ('value',)
    readonly_fields = ('created_at', 'last_seen')

@admin.register(ThreatActor)
class ThreatActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'first_seen')
    search_fields = ('name', 'description')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'threat_actor')
    search_fields = ('name', 'description')

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'status', 'created_at')
    list_filter = ('severity', 'status')
    search_fields = ('title', 'description')

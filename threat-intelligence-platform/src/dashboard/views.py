from django.shortcuts import render
from core.models import IOC, Incident
from django.db.models import Count

def index(request):
    total_iocs = IOC.objects.count()
    malicious_iocs = IOC.objects.filter(reputation_score__gt=0).count()
    recent_incidents = Incident.objects.order_by('-created_at')[:5]
    
    # Simple aggregation for chart
    ioc_types = IOC.objects.values('ioc_type').annotate(count=Count('ioc_type'))
    
    context = {
        'total_iocs': total_iocs,
        'malicious_iocs': malicious_iocs,
        'recent_incidents': recent_incidents,
        'ioc_types': ioc_types,
    }
    return render(request, 'dashboard/index.html', context)

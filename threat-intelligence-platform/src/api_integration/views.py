from rest_framework import viewsets, permissions
from core.models import IOC, ThreatActor, Campaign
from .serializers import IOCSerializer, ThreatActorSerializer, CampaignSerializer

class IOCViewSet(viewsets.ModelViewSet):
    queryset = IOC.objects.all().order_by('-created_at')
    serializer_class = IOCSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = IOC.objects.all()
        ioc_type = self.request.query_params.get('type')
        if ioc_type:
            queryset = queryset.filter(ioc_type=ioc_type)
        return queryset

class ThreatActorViewSet(viewsets.ModelViewSet):
    queryset = ThreatActor.objects.all()
    serializer_class = ThreatActorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

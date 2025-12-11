from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IOCViewSet, ThreatActorViewSet, CampaignViewSet

router = DefaultRouter()
router.register(r'iocs', IOCViewSet)
router.register(r'actors', ThreatActorViewSet)
router.register(r'campaigns', CampaignViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

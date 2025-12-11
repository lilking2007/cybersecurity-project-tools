from rest_framework import serializers
from core.models import IOC, ThreatActor, Campaign

class IOCSerializer(serializers.ModelSerializer):
    class Meta:
        model = IOC
        fields = '__all__'

class ThreatActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatActor
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

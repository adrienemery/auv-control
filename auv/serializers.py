from rest_framework import serializers

from navigation.models import Trip
from navigation.serializers import TripSerializer
from .models import AUV, AUVData


class AUVSerializer(serializers.ModelSerializer):

    active_trip = serializers.SerializerMethodField()

    class Meta:
        model = AUV
        fields = '__all__'
        read_only = ('id',)

    def get_active_trip(self, auv):
        try:
            trip = Trip.objects.get(auv=auv, active=True)
        except Trip.DoesNotExist:
            return None
        else:
            return TripSerializer(trip).data


class AUVDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = AUVData
        fields = '__all__'
        read_only = ('id',)





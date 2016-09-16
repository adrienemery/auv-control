from rest_framework import serializers
from .models import Trip, Waypoint


class WaypointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Waypoint
        fields = ('id', 'lat', 'lng', 'order', 'trip')
        read_only_fields = ('id', 'trip')

    def create(self, validated_data):
        validated_data['trip_id'] = self.context['view'].kwargs['trip_pk']
        return super().create(validated_data)


class TripSerializer(serializers.ModelSerializer):

    waypoints = WaypointSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = ('id', 'name', 'active', 'waypoints', 'auv')
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['auv_id'] = self.context['view'].kwargs['auv_pk']
        return super().create(validated_data)

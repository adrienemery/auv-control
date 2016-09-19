from rest_framework import serializers
from .models import Trip, Waypoint


class WaypointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Waypoint
        fields = ('id', 'lat', 'lng', 'order')
        read_only_fields = ('id', 'trip')

    def create(self, validated_data):
        validated_data['trip_id'] = self.context['view'].kwargs['trip_pk']
        return super().create(validated_data)


class TripSerializer(serializers.ModelSerializer):

    waypoints = WaypointSerializer(many=True, required=False)

    class Meta:
        model = Trip
        fields = ('id', 'name', 'active', 'waypoints')
        read_only_fields = ('id',)

    def create(self, validated_data):
        # pop waypoint data so we can create the Trip first
        waypoints = validated_data.pop('waypoints')
        validated_data['auv_id'] = self.context['view'].kwargs['auv_pk']
        trip = super().create(validated_data)
        waypoints = [Waypoint(trip=trip, **kwargs) for kwargs in waypoints]
        Waypoint.objects.bulk_create(waypoints)
        return trip

    def update(self, instance, validated_data):
        waypoints = validated_data.pop('waypoints')
        # lets be lazy and just delete all waypoints
        # and create fresh ones
        instance.waypoints.all().delete()
        waypoints = [Waypoint(trip=instance, **kwargs) for kwargs in waypoints]
        Waypoint.objects.bulk_create(waypoints)
        return super().update(instance, validated_data)

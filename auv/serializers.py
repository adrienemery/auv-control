from channels import Channel
from rest_framework import serializers, exceptions

from auv_control_api.constants import WAMP_RPC_CHANNEL
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

    def update(self, instance, validated_data):
        # ensure `target_lat` and `target_lng` are set if
        # the mode is set to `move_to_waypoint`
        if validated_data.get('mode') == AUV.MOVE_TO_WAYPOINT:
            if not validated_data.get('target_lat') or not validated_data.get('target_lng'):
                err_msg = 'Must set `target_lat` and `target_lng`'
                raise exceptions.ValidationError(err_msg)

        elif validated_data.get('mode') == AUV.TRIP:
            try:
                Trip.objects.get(auv=instance, active=True)
            except Trip.DoesNotExist:
                err_msg = 'Must have active trip to set mode to `trip`'
                raise exceptions.ValidationError(err_msg)

            content = {
                'procedure': 'com.auv.start_trip',
                'data': {}
            }
            Channel(WAMP_RPC_CHANNEL).send(content)

        instance = super().update(instance, validated_data)
        data = AUVSettingsSerializer(instance).data
        content = {
            'procedure': 'com.auv.update_settings',
            'data': data
        }
        Channel(WAMP_RPC_CHANNEL).send(content)
        return instance


class AUVSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AUV
        fields = ('update_frequency', 'mode', 'target_lat', 'target_lng')
        read_only_fields = fields


class AUVDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = AUVData
        fields = '__all__'
        read_only = ('id',)





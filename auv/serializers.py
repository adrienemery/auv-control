from rest_framework import serializers

from auv_control_api import settings
from .models import AUV, AUVData


class AUVSerializer(serializers.ModelSerializer):

    wamp_url = serializers.SerializerMethodField()
    wamp_realm = serializers.SerializerMethodField()
    api_token = serializers.SerializerMethodField()

    class Meta:
        model = AUV
        fields = ('name', 'description', 'last_seen', 'update_frequency',
                  'auv_id', 'wamp_url', 'wamp_realm', 'api_token')
        read_only = ('id',)

    def get_wamp_url(self, intance):
        return settings.CROSSBAR_URL

    def get_wamp_realm(self, intance):
        return settings.CROSSBAR_REALM

    def get_api_token(self, instance):
        return instance.api_tokens.all().first().token


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





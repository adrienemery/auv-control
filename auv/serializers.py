from rest_framework import serializers

from .models import AUV


class AUVSerializer(serializers.ModelSerializer):

    class Meta:
        model = AUV
        fields = '__all__'


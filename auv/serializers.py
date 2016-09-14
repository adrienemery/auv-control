from rest_framework import serializers

from .models import AUV, AUVData


class AUVSerializer(serializers.ModelSerializer):

    class Meta:
        model = AUV
        fields = '__all__'
        read_only = ('id',)


class AUVDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = AUVData
        fields = '__all__'
        read_only = ('id',)





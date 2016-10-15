from channels import Channel
from django.db.models.signals import post_save
from django.dispatch import receiver

from auv_control_api.constants import WAMP_RPC_CHANNEL
from navigation.models import Trip
from navigation.serializers import TripSerializer


@receiver(post_save, sender=Trip)
def on_trip_post_save(sender, **kwargs):
    """Set the trip on the AUV if this trip is active"""
    instance = kwargs.get('instance')
    if instance.active:
        data = TripSerializer(instance).data
        content = {
            'procedure': 'com.auv.set_trip',
            'data': data
        }
        print(data)
        Channel(WAMP_RPC_CHANNEL).send(content)


from channels import Channel
from django.db.models.signals import post_save
from django.dispatch import receiver

from navigation.models import Trip
from navigation.serializers import WaypointSerializer


# @receiver(post_save, sender=Trip)
# def on_trip_post_save(sender, **kwargs):
#     instance = kwargs.get('instance')
#     if instance.active:
#         waypoints = instance.waypoints.all()
#         data = WaypointSerializer(waypoints, many=True).data
#         content = {
#             'rpc': 'com.auv.start_trip',
#             'data': data
#         }
#         Channel('auv.send').send(content)



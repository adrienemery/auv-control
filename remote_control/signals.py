from django.db.models.signals import post_save
from django.dispatch import receiver

from auv_control_api.constants import WAMP_RPC_CHANNEL
from navigation.models import Trip
from navigation.serializers import TripSerializer


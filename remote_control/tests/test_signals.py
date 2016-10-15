import pytest

from channels.tests import ChannelTestCase
from django.contrib.auth.models import User

from auv_control_api.constants import WAMP_RPC_CHANNEL
from auv.models import AUV
from navigation.models import Trip, Waypoint
from navigation.serializers import TripSerializer

pytestmark = pytest.mark.django_db


class TestChannels(ChannelTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.auv = AUV.objects.create(owner=self.user, name='test')

    def test_on_trip_post_save_active(self):
        waypoint = Waypoint.objects.create(lat='49', lng='120')
        trip = Trip.objects.create(auv=self.auv)
        trip.waypoints.add(waypoint)
        trip.active = True
        trip.save()
        result = self.get_next_message(WAMP_RPC_CHANNEL)
        expected_data = {
            'procedure': 'com.auv.set_trip',
            'data': TripSerializer(trip).data
        }
        self.assertDictEqual(result.content, expected_data)

    def test_on_trip_post_save_inactive(self):
        waypoint = Waypoint.objects.create(lat='49', lng='120')
        trip = Trip.objects.create(auv=self.auv)
        trip.waypoints.add(waypoint)
        trip.save()
        result = self.get_next_message(WAMP_RPC_CHANNEL)
        self.assertIsNone(result)

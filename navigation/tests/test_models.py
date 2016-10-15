import pytest

from auv.models import AUV
from ..models import Trip

pytestmark = pytest.mark.django_db


def test_single_trip_active():
    """Only one trip can be active at a time"""
    auv = AUV.objects.create(name='test')
    trip_a = Trip.objects.create(auv=auv, name='trip a')
    trip_b = Trip.objects.create(auv=auv, name='trip b',
                                 active=True)
    assert trip_b.active is True
    trip_a.active = True
    trip_a.save()
    active_trip = Trip.objects.get(active=True)
    assert trip_a.id == active_trip.id



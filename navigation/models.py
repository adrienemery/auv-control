from django.db import models
from utils.models import BaseModel
from auv.models import AUV


class Trip(BaseModel):
    """Represents a series of Waypoints
    """
    auv = models.ForeignKey(AUV)
    name = models.CharField(max_length=255)
    # only one trip can be active at a time
    active = models.BooleanField(blank=True, default=False)


class Waypoint(BaseModel):
    """Basicaly a Latitite and Longitude

    Multiple waypoints define a trip.
    """
    trip = models.ForeignKey(Trip, blank=True, null=True)
    # trips with multiple waypoints must have an order to know which order
    # to move between the waypoints
    order = models.IntegerField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)


class Location(BaseModel):
    """Store a location for a given AUV.

    Query the latest based on timestamp to know the current location.
    """
    auv = models.ForeignKey(AUV)
    trip = models.ForeignKey(Trip, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(blank=True, null=True)


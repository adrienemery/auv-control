from django.db import models
from utils.models import BaseModel
from auv.models import AUV


class Trip(BaseModel):
    """Represents a series of Waypoints

    Only one trip can be active at a time
    """
    auv = models.ForeignKey(AUV, related_name='trips', on_delete=models.CASCADE,)
    name = models.CharField(max_length=255)
    # only one trip can be active at a time
    active = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # if this trip is active we need to make sure that no other
        # trips are active and if we find one we set it to be
        # inactive which ensures this trip is the only active trip
        if self.active:
            try:
                active_trip = Trip.objects.get(active=True)
            except Trip.DoesNotExist:
                pass
            else:
                active_trip.active = False
                active_trip.save()
        super().save(*args, **kwargs)


class Waypoint(BaseModel):
    """Basicaly a Latitite and Longitude

    Multiple waypoints define a trip.
    """
    trip = models.ForeignKey(
        Trip,
        blank=True,
        null=True,
        related_name='waypoints',
        on_delete=models.CASCADE,
    )
    # trips with multiple waypoints must have an order to know which order
    # to move between the waypoints
    order = models.IntegerField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    def str(self):
        return '{}, {}'.format(self.lat, self.lng)

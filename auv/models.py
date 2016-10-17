from django.contrib.auth.models import User
from django.db import models

from utils.models import BaseModel


class AUV(BaseModel):
    """Primary model representing a single AUV"""
    MANUAL = 'manual'
    LOITER = 'loiter'
    TRIP = 'trip'
    MOVE_TO_WAYPOINT = 'move_to_waypoint'

    MODE_CHOICES = (
        (MANUAL, 'Manual'),
        (LOITER, 'Loiter'),
        (TRIP, 'Trip'),
        (MOVE_TO_WAYPOINT, 'Move To Waypoint')
    )

    owner = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    last_seen = models.DateTimeField(blank=True, null=True,
                                     help_text='updated whenever a '
                                               'heartbeat is recieved')
    mode = models.CharField(max_length=255, choices=MODE_CHOICES,
                            default=MANUAL)
    target_lat = models.FloatField(null=True, blank=True)
    target_lng = models.FloatField(null=True, blank=True)
    update_frequency = models.FloatField(default=1,
                                         help_text='Update frequency in [Hz]')

    def __str__(self):
        return self.name


class AUVData(BaseModel):
    """A log of all sensor data"""
    auv = models.ForeignKey(AUV, blank=True, null=True)

    # battery
    battery_percentage = models.FloatField(blank=True, null=True)
    battery_temperature = models.FloatField(blank=True, null=True)

    # ahrs
    depth = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    heading = models.FloatField(blank=True, null=True)
    roll = models.FloatField(blank=True, null=True)
    pitch = models.FloatField(blank=True, null=True)
    yaw = models.FloatField(blank=True, null=True)

    # gps
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    target_lat = models.FloatField(null=True, blank=True)
    target_lng = models.FloatField(null=True, blank=True)

    # enviornmental data
    air_temperature = models.FloatField(blank=True, null=True)
    water_temperature = models.FloatField(blank=True, null=True)

    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-created',)  # TODO order by timestamp if needed

    @classmethod
    def log(cls, auv, **data):
        return cls.objects.create(auv=auv, **data)

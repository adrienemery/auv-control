from django.contrib.auth.models import User
from django.db import models
from utils.models import BaseModel


class AUV(BaseModel):
    """Primary model representing a single AUV
    """
    owner = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=50, unique=True)
    # human and machine readable address ie. auv.one
    address = models.CharField(max_length=50, unique=True)
    last_seen = models.DateTimeField(blank=True, null=True,
                                     help_text='updated whenever a '
                                               'heartbeat is recieved')
    max_depth = models.FloatField(blank=True, null=True)  # [m]
    max_speed = models.FloatField(blank=True, null=True)  # [m/s]
    max_time_underwater = models.FloatField(blank=True, null=True)  # [ms]
    update_frequency = models.FloatField(blank=True, null=True,
                                         help_text='Update frequency in [Hz]')

    def __str__(self):
        return self.name


class AUVData(BaseModel):
    """A log of all sensor data
    """
    auv = models.ForeignKey(AUV, blank=True, null=True)

    # battery
    battery_percentage = models.FloatField(blank=True, null=True)
    battery_temperature = models.FloatField(blank=True, null=True)

    # ahrs data
    depth = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    heading = models.FloatField(blank=True, null=True)
    roll = models.FloatField(blank=True, null=True)
    pitch = models.FloatField(blank=True, null=True)
    yaw = models.FloatField(blank=True, null=True)

    # enviornmental data
    temperature = models.FloatField(blank=True, null=True)

    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-created',)  # TODO order by timestamp if needed

    @classmethod
    def log(cls, auv, **data):
        return cls.objects.create(auv=auv, **data)

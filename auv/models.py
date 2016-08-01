from django.db import models
from utils.models import BaseModel


class AUV(BaseModel):
    """Primary model representing a single AUV
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=50)
    last_seen = models.DateTimeField(blank=True, null=True,
                                     help_text='updated whenever a heartbeat is recieved')
    max_depth = models.FloatField(blank=True, null=True)  # [m]
    max_speed = models.FloatField(blank=True, null=True)  # [m/s]
    max_time_underwater = models.FloatField(blank=True, null=True)  # [ms]


class AUVData(BaseModel):
    """A log of all sensor data
    """
    auv = models.ForeignKey(AUV, blank=True, null=True)
    depth = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    heading = models.FloatField(blank=True, null=True)
    roll = models.FloatField(blank=True, null=True)
    pitch = models.FloatField(blank=True, null=True)
    yaw = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

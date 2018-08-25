import hashlib
import secrets
import uuid

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

    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
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

    @property
    def auv_id(self):
        """Use the first part of the UUID as the reference id
        """
        return str(self.id).split('-')[0]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # create an api token if none exists
        try:
            AUVToken.objects.get(auv=self)
        except AUVToken.DoesNotExist:
            AUVToken.objects.create(auv=self)


class AUVData(BaseModel):
    """A log of all sensor data"""
    auv = models.ForeignKey(AUV, blank=True, null=True, on_delete=models.CASCADE)

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


class AUVTokenManager(models.Manager):

    def create(self, auv):
        token = secrets.token_hex(16)
        token_hash_hex = hashlib.sha256(token.encode('ascii')).hexdigest()
        super().create(auv=auv, token=token, token_hash=token_hash_hex)
        # Note only the token - not the AUVTokenManager object - is returned
        return token


class AUVToken(BaseModel):

    objects = AUVTokenManager()

    auv = models.ForeignKey(AUV, on_delete=models.CASCADE,
                            related_name='api_tokens')

    # for now store token and hash in db for simplicity but eventually move
    # to only storing the hash and only returing the unhashed token
    # when it is created
    token = models.CharField(max_length=255)
    token_hash = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.auv}-{self.token_hash}'

    @staticmethod
    def hash_token(token):
        return hashlib.sha256(token.encode('ascii')).hexdigest()

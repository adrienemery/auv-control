import asyncio
import logging

from autobahn.asyncio.wamp import ApplicationSession

from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from knox.auth import AuthToken
from rest_framework import exceptions

from auv_control_api.asgi import channel_layer
from auv_control_api.constants import WAMP_RPC_CHANNEL, WAMP_PUBLISH_CHANNEL
from auv.models import AUV
from auv.serializers import AUVDataSerializer, AUVSettingsSerializer
from navigation.models import Trip
from navigation.serializers import TripSerializer

logger = logging.getLogger(__name__)


class RemoteInterface(ApplicationSession):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create a user for authentication
        self.user, _ = User.objects.get_or_create(username='remote')

    def __del__(self):
        """Clean up auth tokens"""
        AuthToken.objects.filter(user=self.user).delete()

    def onConnect(self):
        logger.info('Connecting to {} as {}'.format(self.config.realm, 'backend'))
        self.join(realm=settings.CROSSBAR_REALM, authmethods=['ticket'], authid='backend')

    def onChallenge(self, challenge):
        """Return authentication token when challenged by WAMP router"""
        if challenge.method == 'ticket':
            logger.info("WAMP-Ticket challenge received: {}".format(challenge))
            # create a throw away token
            auth_token = AuthToken.objects.create(user=self.user, expires=None)
            return auth_token
        else:
            raise Exception("Invalid authmethod {}".format(challenge.method))

    async def onJoin(self, details):
        """Subscribe to topics and register RPC's"""
        logger.info("Joined Crossbar Session")
        await self.subscribe(self._handle_auv_connected, 'com.auv.connected')
        await self.subscribe(self._handle_auv_update, 'com.auv.update')
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self._route_wamp_calls(), loop=loop)

    async def _route_wamp_calls(self):
        """Read messages from the channel layer and relay to the WAMP router

        Supported channels:
            wamp.rpc
            wamp.publish

        """
        while True:
            channel, data = channel_layer.receive_many([WAMP_RPC_CHANNEL,
                                                        WAMP_PUBLISH_CHANNEL])
            if channel == WAMP_RPC_CHANNEL:
                if data.get('procedure'):
                    self.call(data.get('procedure'), data.get('data'))
                else:
                    logger.error('Must define a `procedure` to call')

            elif channel == WAMP_PUBLISH_CHANNEL:
                if data.get('topic'):
                    self.publish(data.get('topic'), data.get('data'))
                else:
                    logger.error('Must define a `topic` to publish to')

            await asyncio.sleep(0.01)

    def _handle_auv_update(self, data):
        """Log AUV data to database"""
        auv_id = data.get('auv_id')
        self._update_last_seen(auv_id)
        serializer = AUVDataSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except exceptions.ValidationError as exc:
            logger.error(exc)

    def _handle_auv_connected(self, auv_id):
        """Updates the AUV with latest settings whenever it comes online

        This allows the AUV to drop offline and the operator can still
        update settings, queue trips etc. and whenever the AUV comes
        back online the updates will be pushed out to it.
        """
        logger.info('Auv connected with ID: {}'.format(auv_id))
        self._update_last_seen(auv_id)

        # update AUV with latest settings
        try:
            auv = AUV.objects.get(id=auv_id)
        except AUV.DoesNotExist:
            logger.warning('AUV(id={}) Does Not Exist'.format(auv_id))
            return

        auv_settings_data = AUVSettingsSerializer(auv).data
        self.call('com.auv.update_settings', auv_settings_data)

        # set the active trip if there is one
        try:
            active_trip = Trip.objects.get(active=True)
        except Trip.DoesNotExist:
            active_trip = None
        if active_trip:
            trip_data = TripSerializer(active_trip, allow_null=True).data
        else:
            trip_data = None
        self.call('com.auv.set_trip', trip_data)

    def _update_last_seen(self, auv_id):
        try:
            auv = AUV.objects.get(id=auv_id)
        except AUV.DoesNotExist:
            logger.warning('AUV(id={}) Does Not Exist'.format(auv_id))
            return
        auv.last_seen = timezone.now()
        auv.save()

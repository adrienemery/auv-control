import logging
from autobahn.asyncio.component import Component, run

from django.core.management.base import BaseCommand
from django.conf import settings
from remote_control.remote_control import RemoteInterface


logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = settings.CROSSBAR_URL
        realm = settings.CROSSBAR_REALM
        comp = Component(
            transports=url,
            realm=realm,
            session_factory=RemoteInterface,
        )
        run([comp])

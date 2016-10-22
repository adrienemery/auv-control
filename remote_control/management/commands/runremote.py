import logging
import txaio

txaio.use_asyncio()

from autobahn_autoreconnect import BackoffStrategy, ApplicationRunner
from django.core.management.base import BaseCommand
from django.conf import settings
from remote_control.remote_control import RemoteInterface


logging.basicConfig(level=logging.INFO)


class RetryForever(BackoffStrategy):
    """Retry increasingly until `max_interval` is reached

    Continue retrying forever with a delay of `max_interval`
    """

    def increase_retry_interval(self):
        """Increase retry interval until the max_interval is reached
        """
        self._retry_interval = min(self._retry_interval * self._factor, self._max_interval)

    def retry(self):
        """Retry forever
        """
        return True


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = settings.CROSSBAR_URL
        realm = settings.CROSSBAR_REALM
        retry_strategy = RetryForever(max_interval=60)
        runner = ApplicationRunner(url=url, realm=realm, retry_strategy=retry_strategy)
        runner.run(RemoteInterface)

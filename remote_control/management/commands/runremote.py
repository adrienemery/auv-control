import configparser
import logging

from django.core.management.base import BaseCommand
from remote_control.remote_control import RemoteInterface, ApplicationRunner
from autobahn_autoreconnect import BackoffStrategy


logging.basicConfig(level=logging.INFO)


class RetryForever(BackoffStrategy):
    """Retry increasingly until `max_interval` is reached

    Continue retrying forever with a delay of `max_interval`
    """

    def increase_retry_interval(self):
        """Increase retry interval until the max_interval is reached"""
        self._retry_interval = min(self._retry_interval * self._factor, self._max_interval)

    def retry(self):
        """Retry forever"""
        return True


class Command(BaseCommand):

    def handle(self, *args, **options):

        crossbar_config = configparser.ConfigParser()
        crossbar_config.read('config.ini')
        url = crossbar_config['crossbar']['url']
        realm = crossbar_config['crossbar']['realm']
        retry_strategy = RetryForever(max_interval=60)
        runner = ApplicationRunner(url=url, realm=realm, retry_strategy=retry_strategy)
        runner.run(RemoteInterface)

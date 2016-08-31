import envitro

from pprint import pprint
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from rest_framework import exceptions

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ApplicationError

from knox.auth import TokenAuthentication

AUTH_ID = 'authenticator'
AUTH_TICKET = envitro.str('AUTH_TICKET', '@1ox6*xba-t23l)y_&#_2#7epg-3oc&e@^kmgw7nk*e#g)5f_^')


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # TODO make uri, port, realm settable via args
        pass

    def handle(self, *args, **options):
        url = 'ws://localhost:8080/ws'
        realm = 'realm1'
        runner = ApplicationRunner(url=url, realm=realm)
        runner.run(WAMPAuthenticator)


class WAMPAuthenticator(ApplicationSession):

    def onConnect(self):
        print('Connecting to {} as {}'.format(self.config.realm, AUTH_ID))
        self.join(realm=self.config.realm, authmethods=['ticket'], authid=AUTH_ID)

    def onChallenge(self, challenge):
        if challenge.method == 'ticket':
            print("WAMP-Ticket challenge received: {}".format(challenge))
            return AUTH_TICKET
        else:
            raise Exception("Invalid authmethod {}".format(challenge.method))

    async def onJoin(self, details):

        def authenticate(realm, authid, details):
            ticket = details['ticket']
            print("WAMP-Ticket dynamic authenticator invoked: realm='{}', authid='{}', ticket='{}'".format(realm, authid, ticket))
            pprint(details)

            authenticator = TokenAuthentication()
            try:
                user, auth_token = authenticator.authenticate_credentials(token=ticket)
            except exceptions.AuthenticationFailed:
                print('Authentication failed for {}'.format(authid))
                raise ApplicationError("com.auv.invalid_ticket",
                                       "could not authenticate session - invalid ticket "
                                       "'{}' for principal {}".format(ticket, authid))
            else:
                # TODO store roles in database for different components
                # return default role
                return 'default'

        # register authenticate method
        try:
            await self.register(authenticate, 'com.auv.authenticate')
            print("WAMP-Ticket dynamic authenticator registered!")
        except Exception as e:
            print("Failed to register dynamic authenticator: {0}".format(e))

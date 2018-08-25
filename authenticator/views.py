from knox.auth import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions

from auv.models import AUVToken


token_authenticator = TokenAuthentication()


class ValidateTokenView(APIView):
    """View for validating tokens
    """
    authentication_classes = []
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """Return a 200 if the token is valid
        """
        token = request.data.get('token')
        authid = request.data.get('authid')
        if not token or not authid:
            raise exceptions.ParseError('Must provide `token` and `authid`')

        if authid == 'auv':
            try:
                AUVToken.objects.get(token=token)
            except AUVToken.DoesNotExist:
                pass
            else:
                return Response(data={'role': 'auv'})
        elif authid == 'admin':
            if isinstance(token, str):
                token = token.encode()
            # convert to bytes if token is string
            token_authenticator.authenticate_credentials(token)
            return Response(data={'role': 'auv'})

        raise exceptions.AuthenticationFailed()

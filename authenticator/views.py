from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView


class ValidateTokenView(APIView):
    """View for validating tokens
    """
    authentication_classes = (TokenAuthentication,)

    def post(self, request, format=None):
        """Return a 200 if the token is valid
        """
        return Response()

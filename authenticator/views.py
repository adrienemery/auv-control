from rest_framework.views import APIView
from rest_framework.response import Response

from knox.auth import TokenAuthentication


class ValidateTokenView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (TokenAuthentication,)

    def post(self, request, format=None):
        """
        Return a list of all users.
        """
        return Response()

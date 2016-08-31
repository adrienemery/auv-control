from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status


class Status(APIView):
    """
    View to determine if service is up.
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        return Response(status=status.HTTP_200_OK,
                        data={'status': 'ok'})


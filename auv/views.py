from rest_framework import viewsets, mixins
from knox.auth import TokenAuthentication
from .models import AUV
from .serializers import AUVSerializer


class AUVViewSet(mixins.ListModelMixin,
                 viewsets.GenericViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = AUVSerializer

    def get_queryset(self):
        user = self.request.user
        return AUV.objects.filter(owner_id=user.id)

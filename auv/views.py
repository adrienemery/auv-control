import logging

from rest_framework import viewsets, mixins, exceptions
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import AUV, AUVData
from .serializers import AUVSerializer, AUVDataSerializer

logger = logging.getLogger()


class AUVPermission(BasePermission):

    def has_permission(self, request, view):
        """Requesting user must own auv specified to get access
        """
        auv_id = view.kwargs.get('auv_pk')
        try:
            AUV.objects.get(id=auv_id, owner=request.user)
        except AUV.DoesNotExist:
            logger.warn('User attempted to access an AUV they do no own')
            return False
        return True


class AUVViewSetMixin:
    """Mixin for any ViewSet that has a base url or /api/auv/{auv_id}
    """
    permission_classes = (IsAuthenticated, AUVPermission)

    def get_auv(self):
        user = self.request.user
        auv_pk = self.kwargs.get('auv_pk')
        try:
            return AUV.objects.get(pk=auv_pk, owner=user.pk)
        except AUV.DoesNotExist:
            raise exceptions.NotFound()

    def check_auv_exists(self):
        self.get_auv()


class AUVViewSet(viewsets.ModelViewSet):

    serializer_class = AUVSerializer

    def get_queryset(self):
        user = self.request.user
        return AUV.objects.filter(owner=user)


class AUVDataViewSet(AUVViewSetMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    serializer_class = AUVDataSerializer

    def get_queryset(self):
        auv_id = self.kwargs.get('auv_pk')
        return AUVData.objects.filter(auv_id=auv_id)

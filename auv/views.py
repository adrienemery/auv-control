import logging

from rest_framework import viewsets, mixins
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import AUV, AUVData
from .serializers import AUVSerializer, AUVDataSerializer

logger = logging.getLogger()


class AUVPermission(BasePermission):

    def has_permission(self, request, view):
        """Requesting user must own auv specified to get access"""
        auv_id = view.kwargs.get('auv_pk')
        try:
            AUV.objects.get(auv_id=auv_id, owner=request.user)
        except AUV.DoesNotExist:
            logger.warn('User attempted to access another users auv')
            return False
        return True


class AUVViewSet(mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):

    serializer_class = AUVSerializer

    def get_queryset(self):
        user = self.request.user
        return AUV.objects.filter(owner=user)


class AUVDataViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, AUVPermission)
    serializer_class = AUVDataSerializer

    def get_queryset(self):
        auv_id = self.kwargs.get('auv_pk')
        return AUVData.objects.filter(auv_id=auv_id)

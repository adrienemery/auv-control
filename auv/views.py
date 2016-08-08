from rest_framework import viewsets, mixins, permissions, exceptions
from .models import AUV


class AUVViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user = self.request.user
        return AUV.objects.filter(owner_id=user.id)

from rest_framework import viewsets, mixins, permissions, exceptions
from auv.models import AUV
from .models import Trip, Waypoint, Location


class AUVViewSetMixin:

    def get_auv(self):
        user = self.request.user
        auv_pk = self.kwargs.get('auv_pk')
        try:
            return AUV.objects.get(pk=auv_pk, owner=user.pk)
        except AUV.DoesNotExist:
            raise exceptions.NotFound()

    def check_auv_exists(self):
        self.get_auv()


class TripViewSet(AUVViewSetMixin,
                  viewsets.ModelViewSet):

    def get_queryset(self):
        auv = self.get_auv()
        return Trip.objects.filter(auv=auv)


class WayPointViewSet(AUVViewSetMixin,
                      viewsets.ModelViewSet):

    def get_queryset(self):
        self.check_auv_exists()
        trip_pk = self.kwargs.get('trip_pk')
        return Waypoint.objects.filter(trip=trip_pk)


class LocationViewSet(AUVViewSetMixin,
                      viewsets.ModelViewSet):

    def get_queryset(self):
        auv = self.get_auv()
        trip_pk = self.kwargs.get('trip_pk')
        queryset = Location.objects.filter(auv=auv)
        if trip_pk:
            queryset.filter(trip_pk='trip_pk')
        return queryset


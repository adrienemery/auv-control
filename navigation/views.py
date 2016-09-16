from rest_framework import viewsets, mixins
from auv.views import AUVViewSetMixin

from .serializers import TripSerializer, WaypointSerializer
from .models import Trip, Waypoint, Location


class TripViewSet(AUVViewSetMixin,
                  viewsets.ModelViewSet):

    serializer_class = TripSerializer

    def get_queryset(self):
        auv = self.get_auv()
        return Trip.objects.filter(auv=auv)


class WayPointViewSet(AUVViewSetMixin,
                      viewsets.ModelViewSet):

    serializer_class = WaypointSerializer

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

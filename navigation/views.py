from channels import Channel
from rest_framework import viewsets
from rest_framework.decorators import detail_route

from auv.views import AUVViewSetMixin

from .serializers import TripSerializer, WaypointSerializer
from .models import Trip, Waypoint


class TripViewSet(AUVViewSetMixin,
                  viewsets.ModelViewSet):

    serializer_class = TripSerializer

    def get_queryset(self):
        auv = self.get_auv()
        return Trip.objects.filter(auv=auv)

    @detail_route(methods=['post'])
    def select(self, request, pk=None, **kwargs):
        trip = self.get_object()
        waypoints = trip.waypoints.all()
        data = WaypointSerializer(waypoints, many=True).data
        content = {
            'rpc': 'com.auv.set_trip',
            'data': data
        }
        Channel('auv.send').send(content)


class WayPointViewSet(AUVViewSetMixin,
                      viewsets.ModelViewSet):

    serializer_class = WaypointSerializer

    def get_queryset(self):
        self.check_auv_exists()
        trip_pk = self.kwargs.get('trip_pk')
        return Waypoint.objects.filter(trip=trip_pk)

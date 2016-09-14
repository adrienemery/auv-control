from django.conf.urls import url, include
from rest_framework_nested import routers
from auv.urls import router
from .views import TripViewSet, WayPointViewSet, LocationViewSet


auv_router = routers.NestedSimpleRouter(router, r'auvs', lookup='auv')
# api/auvs/{auv_pk}/trips
auv_router.register(r'trips', TripViewSet, base_name='trips')
# api/auvs/{auv_pk}/locations
auv_router.register(r'locations', LocationViewSet, base_name='locations')

trip_router = routers.NestedSimpleRouter(auv_router, r'trips', lookup='trip')
# api/auvs/{auv_pk}/trips/{trip_pk}/waypoints
trip_router.register(r'waypoints', WayPointViewSet, base_name='waypoints')
# api/auvs/{auv_pk}/trips/{trip_pk}/locations
trip_router.register(r'locations', LocationViewSet, base_name='trip-locations')


urlpatterns = (
    url(r'^', include(auv_router.urls)),
    url(r'^', include(trip_router.urls)),
)

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import AUVViewSet, AUVDataViewSet

router = DefaultRouter()
# api/auvs/
router.register(r'auvs', AUVViewSet, base_name='auvs')

auv_router = routers.NestedSimpleRouter(router, r'auvs', lookup='auv')
# api/auvs/{auv_pk}/data
auv_router.register(r'data', AUVDataViewSet, base_name='auv-data')


urlpatterns = (
    url(r'^', include(router.urls)),
)

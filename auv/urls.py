from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import AUVViewSet

router = DefaultRouter()
# api/auvs/
router.register(r'auvs', AUVViewSet, base_name='auvs')


urlpatterns = (
    url(r'^', include(router.urls)),
)

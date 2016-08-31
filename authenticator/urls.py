from django.conf.urls import url

from .views import ValidateTokenView

urlpatterns = [
    url(r'validate-token', ValidateTokenView.as_view(), name='validate-token'),
]

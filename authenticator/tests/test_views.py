from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from authenticator.views import ValidateTokenView

factory = APIRequestFactory()


def test_validate_token_view_post():
    """Should get a simple 200 response"""
    user = User(username='test')
    view = ValidateTokenView.as_view()
    url = reverse('validate-token')
    request = factory.post(url)
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 200


def test_validate_token_view_invalid_methods():
    """POST should be the only method allowed"""
    user = User(username='test')
    view = ValidateTokenView.as_view()
    url = reverse('validate-token')
    for method in ('get', 'put', 'patch', 'delete'):
        request = getattr(factory, method)(url)
        force_authenticate(request, user=user)
        response = view(request)
        assert response.status_code == 405

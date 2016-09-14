import pytest

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from ..views import AUVViewSet
from ..models import AUV

factory = APIRequestFactory()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return User.objects.create(username='test')


@pytest.fixture
def auv(user):
    return AUV.objects.create(owner=user)


def test_auv_viewset_list(user, auv):
    view = AUVViewSet.as_view({'get': 'list'})
    url = reverse('auvs-list')
    request = factory.get(url)
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == str(auv.id)


def test_auv_viewset_patch(user, auv):
    view = AUVViewSet.as_view({'patch': 'partial_update'})
    kwargs = {'pk': str(auv.id)}
    update_data = {'name': 'Updated Name'}
    url = reverse('auvs-detail', kwargs=kwargs)
    request = factory.patch(url, data=update_data)
    force_authenticate(request, user=user)
    response = view(request, **kwargs)
    assert response.status_code == 200
    assert response.data['name'] == update_data['name']





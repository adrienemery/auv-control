import pytest

from rest_framework import exceptions

from auv.models import AUV
from auv.serializers import AUVSerializer

pytestmark = pytest.mark.django_db


def test_auv_serializer_move_to_waypoint():

    auv = AUV()
    serializer = AUVSerializer(data={'name': 'test',
                                     'mode': AUV.MOVE_TO_WAYPOINT
                                     })
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    with pytest.raises(exceptions.ValidationError):
        serializer.update(auv, validated_data)

from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as DjoserUserSerializer


User = get_user_model()


class UserSerializer(DjoserUserSerializer):

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User._meta.pk.name,
            User.USERNAME_FIELD,
            'first_name',
            'last_name',
        )
        read_only_fields = (User.USERNAME_FIELD,)

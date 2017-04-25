from rest_framework import serializers
from backpocket.users.models import User


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = User
        fields = (
            'id', 'username', 'name', 'email',
            'is_active', 'is_staff', 'date_joined', 'url',
        )
        read_only_fields = ('date_joined', 'is_active', 'url')


# TODO: Group serializer

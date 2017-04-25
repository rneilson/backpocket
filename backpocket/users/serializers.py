from rest_framework import serializers
from backpocket.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'name', 'email',
            'is_active', 'is_staff', 'date_joined',
        )
        read_only_fields = ('date_joined',)


# TODO: Group serializer

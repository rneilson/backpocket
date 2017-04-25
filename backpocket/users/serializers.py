from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.fields import get_error_detail
from backpocket.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    General user model serializer.
    """
    url = serializers.HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = User
        fields = (
            'id', 'username', 'name', 'email',
            'is_active', 'is_staff', 'date_joined', 'url',
        )
        read_only_fields = ('date_joined', 'is_active', 'url')

class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user creation only.
    """
    url = serializers.HyperlinkedIdentityField(view_name='user-detail')
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'name', 'email', 'url',)
        read_only_fields = ('id', 'url',)

    def create(self, validated_data):
        # Get only allowed fields from validated data
        allowed = set(self.Meta.fields) - set(self.Meta.read_only_fields)
        data = { k: v for k, v in validated_data.items() if k in allowed }
        # Create user but don't save yet
        user = User.objects.create_user(commit=False, **data)
        # Validate password using Django validator list (may raise)
        password = validated_data.get('password')
        try:
            password_validation.validate_password(password, user=user)
        except DjangoValidationError as e:
            self._errors = {'password': get_error_detail(e)}
            raise serializers.ValidationError(self.errors)
        # Now save and return
        user.save()
        return user
    

# TODO: Group serializer

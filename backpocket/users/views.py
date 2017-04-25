from rest_framework import viewsets
from backpocket.users.models import User
from backpocket.users.serializers import (
    UserSerializer, CreateUserSerializer
)
from backpocket.users.permissions import (
    UserObjectPermissions, UserObjectPermissionFilter
)


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for viewing, editing, and adding users.
    """
    permission_classes = [UserObjectPermissions]
    filter_backends = [UserObjectPermissionFilter]
    queryset = User.objects.all()

    serializer_class = UserSerializer
    serializer_map = {
        'create': CreateUserSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    # TODO: user groups detail view
    # TODO: user permissions detail view
    # TODO: set password detail view
    # TODO: reset password detail view
    # TODO: activate detail view

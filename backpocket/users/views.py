from rest_framework import viewsets
from backpocket.users.models import User
from backpocket.users.serializers import UserSerializer
from backpocket.users.permissions import (
    UserObjectPermissions, UserObjectPermissionFilter
)


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for viewing, editing, and adding users.
    """
    permission_classes = [UserObjectPermissions]
    filter_backends = [UserObjectPermissionFilter]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # TODO: user groups detail view
    # TODO: user permissions detail view
    # TODO: set password detail view
    # TODO: reset password detail view
    # TODO: activate detail view

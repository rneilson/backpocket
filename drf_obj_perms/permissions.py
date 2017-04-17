"""
Provides method- and action-based permission policies for DRF.
"""

from django.http import Http404

from rest_framework import exceptions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class ModelObjectPermissions(BasePermission):
    """
    Model- and object-based permissions. Based on DRF's
    DjangoModelPermissions, modified for separate general
    and object-specific permission mapping.
    """

    # Map methods into required permission codes.
    # Override this if you need to also provide 'view' permissions,
    # or if you want to provide custom permission codes.
    perms_map = {
        'GET': (),
        'OPTIONS': (),
        'HEAD': (),
        'POST': ('%(app_label)s.add_%(model_name)s',),
        'PUT': (),
        'PATCH': (),
        'DELETE': (),
    }

    # Map methods into required object permission codes.
    # Override this if you need to also provide 'view' permissions,
    # or if you want to provide custom permission codes.
    obj_perms_map = {
        'GET': (),
        'OPTIONS': (),
        'HEAD': (),
        'POST': (),
        'PUT': ('%(app_label)s.change_%(model_name)s',),
        'PATCH': ('%(app_label)s.change_%(model_name)s',),
        'DELETE': ('%(app_label)s.delete_%(model_name)s',),
    }

    # Lookup keys for obj_perms_map to check read-only permission
    # when determining whether to raise a 404 or 403. Override
    # if also overriding .get_perm_lookup_key().
    # Set obj_read_only_lookup_key to False to skip check.
    obj_read_only_lookup_keys = SAFE_METHODS
    obj_read_only_lookup_key = 'GET'

    # Set to False if 
    authenticated_users_only = True

    def get_perm_lookup_key(self, request, view):
        """
        Provide key to use when looking up required permissions.
        By default, this is the request HTTP method. Override if
        using different criteria for permission mapping.
        """
        return request.method

    def get_required_permissions(self, lookup_key, model_cls,
                                 request=None, attr_name='perms_map'):
        """
        Given a model and a lookup key, return the list of permission
        codes that the user is required to have from the given mapping
        attribute name (default 'perms_map').
        """
        perms_map = getattr(self, attr_name)

        if lookup_key not in perms_map:
            raise exceptions.MethodNotAllowed(
                request.method if request else lookup_key
            )

        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }

        return [perm.format(**kwargs) for perm in perms_map[lookup_key]]

    def get_view_queryset(self, request, view):
        """
        Common method to get queryset from view.
        """
        if hasattr(view, 'get_queryset'):
            queryset = view.get_queryset()
        else:
            queryset = getattr(view, 'queryset', None)

        assert queryset is not None, (
            'Cannot apply {0} on a view that '
            'does not set `.queryset` or have a `.get_queryset()` method.'
            .format(self.__class__.__name__)
        )

        return queryset


    def has_permission(self, request, view):
        # Workaround to ensure model permissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        lookup_key = self.get_perm_lookup_key(request, view)
        model_cls = self.get_view_queryset(request, view).model
        user = request.user
        perms = self.get_required_permissions(
            lookup_key, model_cls, request=request, attr_name='perms_map'
        )

        return (
            user and
            (user.is_authenticated or not self.authenticated_users_only) and
            user.has_perms(perms)
        )

    def has_object_permission(self, request, view, obj):
        lookup_key = self.get_perm_lookup_key(request, view)
        model_cls = self.get_view_queryset(request, view).model
        user = request.user
        perms = self.get_required_permissions(
            lookup_key, model_cls, request=request, attr_name='obj_perms_map'
        )

        if not user.has_perms(perms, obj):
            # If the user does not have permissions we need to determine if
            # they have read permissions to see 403, or not, and simply see
            # a 404 response.
            if self.obj_read_only_lookup_key is not False:
                if lookup_key in self.obj_read_only_lookup_keys:
                    # Read permissions already checked and failed, no need
                    # to make another lookup.
                    raise Http404

                read_perms = self.get_required_permissions(
                    self.obj_read_only_lookup_key, model_cls,
                    request=request, attr_name='obj_perms_map'
                )
                if not user.has_perms(read_perms, obj):
                    raise Http404

            # Has read permissions.
            return False

        return True


class ActionModelObjectPermissions(ModelObjectPermissions):
    """
    As with ModelObjectPermissions, but using a view's
    'action' attribute instead of HTTP request method.
    """
    perms_map = {
        'list': (),
        'create': ('%(app_label)s.add_%(model_name)s',),
        'retrieve': (),
        'update': (),
        'partial_update': (),
        'destroy': (),
        'metadata': (),
    }

    obj_perms_map = {
        'retrieve': (),
        'update': ('%(app_label)s.change_%(model_name)s',),
        'partial_update': ('%(app_label)s.change_%(model_name)s',),
        'destroy': ('%(app_label)s.delete_%(model_name)s',),
        'metadata': (),
    }

    obj_read_only_lookup_keys = ('retrieve', 'metadata')
    obj_read_only_lookup_key = 'retrieve'

    def get_perm_lookup_key(self, request, view):
        # Bit of a workaround for HEAD being automatically mapped
        # to GET in DRF viewsets, but not assigned GET's action
        action = view.action
        if action is None and request.method.lower() == 'head':
            return view.action_map.get('get')
        return action


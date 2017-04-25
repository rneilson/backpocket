"""
Provides method- and action-based queryset filtering
for object permissions.
"""
from rest_framework import exceptions
from rest_framework.filters import BaseFilterBackend

from obj_perms.filters import filter_queryset as obj_filter_queryset


class ActionObjectPermissionsFilter(BaseFilterBackend):
    """
    Filter queryset based on view action and object permission filters.
    """

    # Map view actions into required permission codes.
    # Override this if you need to also provide 'view' permissions,
    # or if you want to provide custom permission codes.
    perms_map = {
        'list': (),
        'create': (),
        'retrieve': (),
        'update': (),
        'partial_update': (),
        'destroy': (),
        'metadata': (),
    }

    # Override and set to True to return queryset unchanged if
    # action not found in perms_map or permission not found on
    # the model's ObjectPermissionsFilter attribute
    default_queryset_unfiltered = False

    def filter_queryset(self, request, queryset, view):
        # Bit of a workaround for HEAD being automatically mapped
        # to GET in DRF viewsets, but not assigned GET's action
        action = view.action
        if action is None and request.method.lower() == 'head':
            action = view.action_map.get('get')

        perms = self.perms_map.get(action)

        # Action not found in perms map
        if perms is None:
            if self.default_queryset_unfiltered:
                return queryset
            # Otherwise raise exception
            raise exceptions.MethodNotAllowed(request.method)

        # Short-circuit empty perms set
        if not perms:
            return queryset

        meta = queryset.model._meta
        kwargs = {
            'app_label': meta.app_label,
            'model_name': meta.model_name
        }
        perms = [perm.format(**kwargs) for perm in perms]
        user = request.user

        return obj_filter_queryset(
            user, perms, queryset, default=self.default_queryset_unfiltered
        )

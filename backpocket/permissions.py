from drf_obj_perms.permissions import ActionModelObjectPermissions
from drf_obj_perms.filters import ActionObjectPermissionsFilter

class BaseActionObjectPermissions(ActionModelObjectPermissions):
    """
    Slightly modified ActionModelObjectPermissions to add view perms.
    """
    perms_map = {
        'list': (),
        'create': ('{app_label}.add_{model_name}',),
        'retrieve': (),
        'update': (),
        'partial_update': (),
        'destroy': (),
        'metadata': (),
    }

    obj_perms_map = {
        'retrieve': ('{app_label}.view_{model_name}',),
        'update': ('{app_label}.change_{model_name}',),
        'partial_update': ('{app_label}.change_{model_name}',),
        'destroy': ('{app_label}.delete_{model_name}',),
        'metadata': ('{app_label}.view_{model_name}',),
    }


class BaseActionObjectPermissionFilter(ActionObjectPermissionsFilter):
    """
    Slightly modified ActionObjectPermissionsFilter to add view perms.
    """
    perms_map = {
        'list': ('{app_label}.view_{model_name}',),
        'create': (),
        'retrieve': (),
        'update': (),
        'partial_update': (),
        'destroy': (),
        'metadata': ('{app_label}.view_{model_name}',),
    }

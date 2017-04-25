from backpocket.permissions import (
    BaseActionObjectPermissions, BaseActionObjectPermissionFilter
)


class UserObjectPermissions(BaseActionObjectPermissions):
    """
    BaseActionObjectPermissions updated with additional actions.
    """
    perms_map = {
        **BaseActionObjectPermissions.perms_map,
        'activate': (),
        'password': (),
        'reset_password': (),
        'groups': (),
        'permissions': (),
    }

    obj_perms_map = {
        **BaseActionObjectPermissions.obj_perms_map,
        'activate': ('{app_label}.set_user_active',),
        'password': ('{app_label}.set_user_password',),
        'reset_password': ('{app_label}.reset_user_password',),
        'groups': ('{app_label}.change_user_groups',),
        'permissions': ('{app_label}.change_user_permissions',),
    }


class UserObjectPermissionFilter(BaseActionObjectPermissionFilter):
    """
    BaseActionObjectPermissionFilter updated with additional actions.
    """
    perms_map = {
        **BaseActionObjectPermissionFilter.perms_map,
        'activate': (),
        'password': (),
        'reset_password': (),
        'groups': (),
        'permissions': (),
    }

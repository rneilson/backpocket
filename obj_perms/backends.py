# User model mixins

from .permissions import ObjectPermissionTester

class ObjectPermissionsBackend:
    """
    Backend to check object permissions to a user model.
    Only use in conjunction with standard PermissionsMixin or
    equivalent which checks all auth backends.
    """

    def authenticate(self, request, **kwargs):
        # Never authenticate through this backend
        return None
    
    def has_perm(self, user_obj, perm, obj=None):
        try:
            obj_perm = ObjectPermissionTester(obj)
            if obj_perm.has_perm(user_obj, perm, obj):
                return True
        except AttributeError:
            pass

        return False

    def get_all_permissions(self, user_obj, obj=None):
        try:
            obj_perm = ObjectPermissionTester(obj)
            perms = obj_perm.get_object_permissions(user_obj, obj)
        except AttributeError:
            perms = set()

        return perms

    # TODO: get_group_permissions()?
    # TODO: get_user_permissions() separately?

# User model mixins

from obj_perms.permissions import has_obj_perm, get_all_object_permissions

class ObjectPermissionsBackend:
    """
    Backend to check object permissions to a user model.
    Only use in conjunction with standard PermissionsMixin or
    equivalent which checks all auth backends.
    """

    DEFAULT_PERMISSION = False
    DEFAULT_ATTR_NAME = None
    ALLOW_ANONYMOUS_USER = False

    def _check_user(self, user_obj):
        if not user_obj:
            return False
        return (user_obj.is_authenticated or self.ALLOW_ANONYMOUS_USER)

    def authenticate(self, request, **kwargs):
        # Never authenticate through this backend
        return None
    
    def has_perm(self, user_obj, perm, obj=None):
        if not self._check_user(user_obj):
            return False

        kwargs = { 'default': self.DEFAULT_PERMISSION }

        if self.DEFAULT_ATTR_NAME is not None:
            kwargs['attr_name'] = self.DEFAULT_ATTR_NAME

        return has_obj_perm(user_obj, perm, obj, **kwargs)

    def get_all_permissions(self, user_obj, obj=None):
        if not self._check_user(user_obj):
            return set()

        kwargs = { 'default': self.DEFAULT_PERMISSION }

        if self.DEFAULT_ATTR_NAME is not None:
            kwargs['attr_name'] = self.DEFAULT_ATTR_NAME

        return get_all_object_permissions(user_obj, obj, **kwargs)

    # TODO: get_group_permissions()?
    # TODO: get_user_permissions() separately?

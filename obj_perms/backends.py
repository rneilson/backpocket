# User model mixins

from obj_perms.permissions import has_obj_perm, get_all_object_permissions
from obj_perms.utils import available_permissions

class ObjectPermissionsBackend:
    """
    Backend to check object permissions to a user model.
    Only use in conjunction with a user model which includes
    the standard PermissionsMixin (or equivalent) and provides
    'has_perm()' and 'get_all_permissions()' attributes.
    """

    # Override this to use a different model attribute name for
    # checking object permissions (default 'ObjectPermissions').
    DEFAULT_ATTR_NAME = None

    # Override this if object permissions are to be implicitly
    # granted unless specifically denied (use with caution!).
    DEFAULT_PERMISSION = False

    # Override this to delegate permission checks for 
    # unauthenticated users to permission-specific method(s).
    ALLOW_ANONYMOUS_USER = False

    # Override this to also check permissions which would be
    # granted with obj=None. This can be used as a shortcut to
    # calling 'user.has_perm(perm, obj=None)' in all permission-
    # specific methods. Requires an additional authentication
    # backend which implements at minimum 'has_perm()' and
    # 'get_all_permissions()'.
    INCLUDE_GENERAL_PERMISSIONS = False

    def _check_user(self, user_obj):
        if not user_obj or not user_obj.is_active:
            return False
        return (user_obj.is_authenticated or self.ALLOW_ANONYMOUS_USER)

    def authenticate(self, request, **kwargs):
        # Never authenticate through this backend
        return None
    
    def has_perm(self, user_obj, perm, obj=None):
        # Ensure valid user given
        if not self._check_user(user_obj):
            return False

        kwargs = { 'default': self.DEFAULT_PERMISSION }

        if self.DEFAULT_ATTR_NAME is not None:
            kwargs['attr_name'] = self.DEFAULT_ATTR_NAME

        # Will return default if no object given
        user_has_perm = has_obj_perm(user_obj, perm, obj, **kwargs)

        # Otherwise check for permission excluding object
        if (obj is not None and
                not user_has_perm and
                self.INCLUDE_GENERAL_PERMISSIONS):
            user_has_perm = user_obj.has_perm(perm, obj=None)

        return user_has_perm

    def get_all_permissions(self, user_obj, obj=None):
        # Ensure valid user given, short-circuit obj=None case
        if not self._check_user(user_obj) or not obj:
            return set()

        kwargs = { 'default': self.DEFAULT_PERMISSION }

        if self.DEFAULT_ATTR_NAME is not None:
            kwargs['attr_name'] = self.DEFAULT_ATTR_NAME

        # Will return empty set if object not given
        user_perms = get_all_object_permissions(user_obj, obj, **kwargs)

        # Also check for permissions excluding object
        if self.INCLUDE_GENERAL_PERMISSIONS:
            for perm in available_permissions(obj, prepend_label=True):
                if user_obj.has_perm(perm):
                    user_perms.add(perm)

        return user_perms

    # TODO: get_group_permissions()?
    # TODO: if so, separate get_user_permissions()?

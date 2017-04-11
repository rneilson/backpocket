# Uses inner classes for models to specify object permission checking.
# Include 'ObjectPermissions' nested class in model definition with
# methods named by desired permission codename.

from .utils import ObjectPermissionsBase

class ObjectPermissionTester(ObjectPermissionsBase):
    """
    User permission checker for given object.
    """

    def __init__(self, model, class_name='ObjectPermissions'):
        super().__init__(self, model, class_name)

        # Get default result
        self.DEFAULT_PERMISSION = getattr(
            obj_perms, 'DEFAULT_PERMISSION', False
        )

    def has_perm(self, user, perm, obj):
        """
        Check if user has perm for obj.
        """

        app_label, codename = self._split_perm(perm)

        # TODO: check perm cache
        check_perm = getattr(self.obj_perms, codename, None)

        # Return default if codename not defined
        if check_perm is None:
            return self.DEFAULT_PERMISSION

        return check_perm(user, perm, obj)

    def has_perms(self, user, perms, obj):
        return all(self.has_perm(user, perm, obj) for perm in perms)

    def get_object_permissions(self, user, obj):
        return set(
            '{0}.{1}'.format(self.app_label, perm)
            for perm in self.perms if self.has_perm(user, perm, obj)
        )

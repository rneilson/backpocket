# Uses inner classes for models to specify object permission filtering.
# Include 'ObjectPermissionFilters' nested class in model definition
# with methods named by desired permission codename.

from .utils import ObjectPermissionsBase

class ObjectPermissionFilter(ObjectPermissionsBase):
    """
    User permission filter for given model.
    """

    def __init__(self, model, class_name='ObjectPermissionFilters'):
        super().__init__(self, model, class_name)

        # Get default filter (True for all, False for none)
        self.DEFAULT_PERMISSION = getattr(
            obj_perms, 'DEFAULT_PERMISSION', True
        )
    
    def filter_queryset(self, user, perms, queryset):
        """
        Filter queryset by user and required perms.
        """

        if isinstance(perms, str):
            perms = (perms,)

        for perm in perms:
            app_label, codename = self._split_perm(perm)

            # TODO: check queryset cache
            filter_perm = getattr(self.obj_perms, codename, None)

            # Return default if codename not defined
            if filter_perm is not None:
                queryset = filter_perm(user, perm, queryset)
            else if not self.DEFAULT_PERMISSION:
                queryset = queryset.none()
                # Short-circuit here, queryset already empty
                break

        return queryset


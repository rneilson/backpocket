# Uses inner classes for models to specify object permission filtering.
# Include 'ObjectPermissionFilters' nested class in model definition
# with methods named by desired permission codename. Each method should
# have the signature 'codename(user, queryset)'.

from obj_perms.utils import split_perm


DEFAULT_ATTR = 'ObjectPermissionFilters'


def filter_queryset(self, user, perms, queryset,
                    default=False, attr_name=DEFAULT_ATTR):
    """
    Filter queryset by user and required permission(s).
    If default is True, queryset will be unchanged if a permission
    is not found; if False, queryset.none() will be returned.
    """
    model = queryset.model

    try:
        filters_obj = getattr(model, attr_name)
    except AttributeError:
        return queryset if default else queryset.none()

    # Turn single perm into an iterable to keep everything simple
    if isinstance(perms, str):
        perms = (perms,)

    for perm in perms:
        app_label, codename = split_perm(model, perm)

        try:
            # TODO: check queryset cache
            queryset = getattr(filters_obj, codename)(user, queryset)
        except AttributeError:
            # Return default if codename not defined
            if not default:
                queryset = queryset.none()
                # Short-circuit here, queryset already empty
                break

    return queryset

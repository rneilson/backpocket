# Uses inner classes for models to specify object permission checking.
# Include 'ObjectPermissions' nested class in model definition with
# methods named by desired permission codename. Each method should have
# the signature 'codename(user, obj)'.

from django.core.exceptions import PermissionDenied
from obj_perms.utils import split_perm, available_permissions


DEFAULT_ATTR = 'ObjectPermissions'


def has_obj_perm(user_obj, perm, obj, default=False,
                 attr_name=DEFAULT_ATTR, obj_perms=None):
    try:
        if obj_perms is None:
            obj_perms = getattr(obj, attr_name)

        app_label, codename = split_perm(obj, perm)

        # TODO: check perm cache
        return getattr(obj_perms, codename)(user_obj, obj)

    except AttributeError:
        # Return default if no object permissions defined
        # or object permissions does not define perm
        return default


def has_obj_perms(user_obj, perm_list, obj,
                  default=False, attr_name=DEFAULT_ATTR):
    # Prefetch obj_perms
    try:
        obj_perms = getattr(obj, attr_name)
    except AttributeError:
        return default

    for perm in perm_list:
        # Let PermissionDenied bubble
        has_perm = has_obj_perm(
            user_obj, perm, obj, default, attr_name, obj_perms
        )
        # Short-circuit return if any permission not granted
        if not has_perm:
            return False

    return True


def get_all_object_permissions(user_obj, obj, default=False,
                               prepend_label=True, attr_name=DEFAULT_ATTR):
    # Prefetch obj_perms
    try:
        obj_perms = getattr(obj, attr_name)
    except AttributeError:
        return default

    perm_list = set()

    for perm in available_permissions(obj, prepend_label):
        try:
            # Use prefetched obj_perms instead of getattr() every time
            has_perm = has_obj_perm(
                user_obj, perm, obj, default, attr_name, obj_perms
            )
            if has_perm:
                perm_list.add(perm)

        except PermissionDenied:
            # PermissionDenied is to short-circuit backend checks,
            # so it doesn't apply here
            pass

    return perm_list


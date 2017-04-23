# Object permission backend(s), Backpocket-specific

from obj_perms.backends import ObjectPermissionsBackend as BaseObjPermsBackend

class ObjectPermissionsBackend(BaseObjPermsBackend):
    """
    Object permissions backend, Backpocket settings
    """
    INCLUDE_GENERAL_PERMISSIONS = True

# Utility functions used by other sub-modules

from django.contrib.auth import get_permission_codename

# Easier to do what 'migrate' does than fetch from db
def get_available_permissions(model):
    """
    Gets valid permissions for model.
    """
    meta = model._meta
    perms = set(
        get_permission_codename(action, meta)
        for action in meta.default_permissions
    )
    perms.update(name for name, desc in meta.permissions)
    # TODO: cache available permissions per-model
    return perms


class ObjectPermissionsBase(object):
    """
    Base class for object permission testers/checkers.
    """

    def __init__(self, model, class_name):
        self.model = model
        # Get app label, model name, permissions
        meta = model._meta
        self.app_label = meta.app_label
        self.model_name = meta.model_name
        # TODO: cache available permissions per-model
        self.perms = get_available_permissions(model)
        # Get object permissions nested class from model
        try:
            obj_perms = getattr(model, class_name)
        except AttributeError as e:
            raise AttributeError(
                "No '{0}' class found on model '{1}'"
                .format(class_name, self.model_name)
            )
        self.obj_perms = obj_perms

    def _split_perm(self, perm):
        """
        Ensures perm is a valid permission for this model.
        Returns (app_label, codename) tuple.
        """

        app_label, codename = perm.split('.')

        if app_label != self.app_label:
            raise ValueError(
                "Permission '{0}' doesn't belong to app '{1}'"
                .format(perm, self.app_label)
            )

        if codename not in self.perms:
            raise ValueError(
                "Invalid permission codename '{0}' for model '{1}'"
                .format(codename, self.model_name)
            )

        return app_label, codename

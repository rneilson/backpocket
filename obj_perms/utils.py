# Utility functions used by other sub-modules

from django.contrib.auth import get_permission_codename

# Easier to do what 'migrate' does than fetch from db
def available_permissions(model):
    """
    Gets valid permissions for model. Does *not* prepend app label.
    """
    meta = model._meta
    perms = set(
        get_permission_codename(action, meta)
        for action in meta.default_permissions
    )
    perms.update(name for name, _ in meta.permissions)
    # TODO: cache available permissions per-model
    return perms


class ObjectPermissionsBase(object):
    """
    Base class for object permission testers/checkers.
    """

    def __init__(self, model, class_name):
        self.model = model
        self.app_label = model._meta.app_label
        # Get object permissions nested class from model
        # Let AttributeError bubble
        self.obj_perms = getattr(model, class_name)

    def _split_perm(self, perm):
        """
        Ensures perm is a valid permission for this model.
        Returns (app_label, codename) tuple.
        """
        app_label, codename = perm.split('.', maxsplit=1)

        if app_label != self.app_label:
            raise ValueError(
                "Permission '{0}' doesn't belong to app '{1}'"
                .format(perm, self.app_label)
            )

        # TODO: check cached available permissions
        return app_label, codename

    def get_available_permissions(self):
        """
        Gets valid permissions for model, including app label.
        """
        return set(
            '{0}.{1}'.format(self.app_label, perm)
            for perm in available_permissions(self.model)
        )

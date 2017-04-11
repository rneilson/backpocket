# Utility functions used by other sub-modules

from django.contrib.auth import get_permission_codename

# Easier to do what 'migrate' does than fetch from db
def available_permissions(model, prepend_label=False):
    """
    Gets valid permissions for model. Prepends app label if
    prepend_label is True.
    """
    meta = model._meta
    perms = set(
        get_permission_codename(action, meta)
        for action in meta.default_permissions
    )
    perms.update(name for name, _ in meta.permissions)
    if prepend_label:
        app_label = model._meta.app_label
        perms = set('{0}.{1}'.format(app_label, perm) for perm in perms)

    # TODO: cache available permissions per-model
    return perms

def split_perm(model, perm, check_valid=False, check_list=None):
    """
    Ensures perm is a valid permission for this model.
    Returns (app_label, codename) tuple.
    """
    model_app = model._meta.app_label
    app_label, codename = perm.split('.', maxsplit=1)

    if app_label != model_app:
        raise ValueError(
            "Permission '{0}' doesn't belong to app '{1}'"
            .format(perm, model_app)
        )

    if check_valid:
        if not check_list:
            check_list = available_permissions(model)
        if codename not in check_list:
            raise ValueError(
                "Permission '{0}' not valid for app '{1}'"
                .format(perm, model_app)
            )

    # TODO: check cached available permissions
    return app_label, codename


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
        return split_perm(self.model, perm)

    def get_available_permissions(self, prepend_label=True):
        """
        Gets valid permissions for model, including app label.
        """
        return available_permissions(self.model, prepend_label)

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
        app_label = meta.app_label
        perms = set('{0}.{1}'.format(app_label, perm) for perm in perms)

    # TODO: cache available permissions per-model
    return perms

def split_perm(model, perm, check_list=False):
    """
    Ensures perm is a valid permission for this model.
    Returns (app_label, codename) tuple.
    """
    try:
        app_label, codename = perm.split('.', maxsplit=1)
    except ValueError:
        app_label, codename = None, perm

    model_app = model._meta.app_label
    if app_label and app_label != model_app:
        raise ValueError(
            "Permission '{0}' doesn't belong to app '{1}'"
            .format(perm, model_app)
        )

    if check_list:
        if check_list is True:
            check_list = available_permissions(model)
        if codename not in check_list:
            raise ValueError(
                "Permission '{0}' not valid for app '{1}'"
                .format(perm, model_app)
            )

    # TODO: check cached available permissions
    return app_label, codename


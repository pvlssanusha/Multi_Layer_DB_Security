from .models import UserRole, RolePermission, Permission


def get_user_role(user):
    """
    Returns the Role object assigned to the user.
    """
    try:
        return UserRole.objects.get(user=user).role
    except UserRole.DoesNotExist:
        return None


def is_allowed(user, action_name):
    """
    Checks if a user has permission for a given action
    by querying RolePermission table.
    """

    role = get_user_role(user)
    if not role:
        return False

    try:
        permission = Permission.objects.get(name=action_name)
    except Permission.DoesNotExist:
        return False

    return RolePermission.objects.filter(
        role=role,
        permission=permission
    ).exists()
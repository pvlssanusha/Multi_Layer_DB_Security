from Secure.models import UserRole, RolePermission


def is_query_allowed(user, query_type: str) -> bool:
    """
    Check whether a user is allowed to execute a query type
    based on RBAC rules.
    """

    # Superusers are always allowed
    if user.is_superuser:
        return True

    query_type = query_type.upper()

    # Get all roles assigned to user
    user_roles = UserRole.objects.filter(user=user).values_list(
        'role_id', flat=True
    )

    if not user_roles:
        return False

    # Check if any role has required permission
    allowed = RolePermission.objects.filter(
        role_id__in=user_roles,
        permission__name=query_type
    ).exists()

    return allowed

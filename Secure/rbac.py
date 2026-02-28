from .models import UserRole

ROLE_PERMISSIONS = {
    "Admin": {"SELECT", "INSERT", "UPDATE", "DELETE"},
    "Analyst": {"SELECT"},
    "User": {"SELECT"},
}

def get_user_role(user):
    try:
        return UserRole.objects.get(user=user).role.role_name
    except UserRole.DoesNotExist:
        return None

def is_allowed(user, action):
    role = get_user_role(user)
    if not role:
        return False
    return action in ROLE_PERMISSIONS.get(role, set())

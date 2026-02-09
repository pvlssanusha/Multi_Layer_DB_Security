from django.core.management.base import BaseCommand
from Secure.models import Role, Permission, RolePermission


class Command(BaseCommand):
    help = "Create default RBAC roles and permissions"

    def handle(self, *args, **kwargs):
        # -----------------------------
        # Define defaults
        # -----------------------------
        roles = {
            "Admin": ["SELECT", "INSERT", "UPDATE", "DELETE"],
            "Analyst": ["SELECT"],
            "User": ["SELECT", "INSERT"],
        }

        # -----------------------------
        # Create Permissions
        # -----------------------------
        permission_objects = {}
        for perm_name in ["SELECT", "INSERT", "UPDATE", "DELETE"]:
            perm, created = Permission.objects.get_or_create(
                name=perm_name,
                defaults={"description": f"{perm_name} permission"}
            )
            permission_objects[perm_name] = perm

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created permission: {perm_name}")
                )

        # -----------------------------
        # Create Roles and Assign Permissions
        # -----------------------------
        for role_name, perms in roles.items():
            role, created = Role.objects.get_or_create(
                role_name=role_name,
                defaults={"description": f"{role_name} role"}
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created role: {role_name}")
                )

            for perm_name in perms:
                RolePermission.objects.get_or_create(
                    role=role,
                    permission=permission_objects[perm_name]
                )

        self.stdout.write(
            self.style.SUCCESS("Default RBAC roles and permissions created successfully.")
        )

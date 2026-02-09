from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from Secure.models import Role, UserRole


@receiver(post_save, sender=User)
def assign_admin_role_to_superuser(sender, instance, created, **kwargs):
    """
    Automatically assign Admin role to superusers
    """
    if instance.is_superuser:
        try:
            admin_role = Role.objects.get(role_name="Admin")
            UserRole.objects.get_or_create(
                user=instance,
                role=admin_role
            )
        except Role.DoesNotExist:
            # Admin role not created yet
            pass

from django.db import models
from django.contrib.auth.models import User

# -----------------------------
# RBAC MODELS
# -----------------------------

class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    allowed_ip = models.GenericIPAddressField(null=True, blank=True)
    login_start_time = models.TimeField(null=True, blank=True)
    login_end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.role_name


class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')


# -----------------------------
# QUERY LOGGING & SECURITY
# -----------------------------

class SQLQueryLog(models.Model):
    QUERY_TYPES = [
        ('SELECT', 'SELECT'),
        ('INSERT', 'INSERT'),
        ('UPDATE', 'UPDATE'),
        ('DELETE', 'DELETE'),
        ('OTHER', 'OTHER'),
    ]

    DECISION_CHOICES = [
        ('ALLOWED', 'ALLOWED'),
        ('BLOCKED', 'BLOCKED'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    query_text = models.TextField()
    query_type = models.CharField(max_length=10, choices=QUERY_TYPES)
    
    is_allowed_by_rbac = models.BooleanField()
    is_malicious_ml = models.BooleanField()
    
    final_decision = models.CharField(
        max_length=10,
        choices=DECISION_CHOICES
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.final_decision} - {self.timestamp}"


class MLDetectionResult(models.Model):
    PREDICTION_CHOICES = [
        ('BENIGN', 'BENIGN'),
        ('MALICIOUS', 'MALICIOUS'),
    ]

    query_log = models.OneToOneField(
        SQLQueryLog,
        on_delete=models.CASCADE,
        related_name='ml_result'
    )
    prediction = models.CharField(
        max_length=10,
        choices=PREDICTION_CHOICES
    )
    confidence_score = models.FloatField()
    model_version = models.CharField(max_length=50)
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prediction} ({self.confidence_score})"
    
class SecureRecord(models.Model):
    name = models.CharField(max_length=100)
    secret_data = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

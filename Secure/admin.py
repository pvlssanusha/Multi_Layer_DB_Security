from django.contrib import admin
from .models import *

# -----------------------------
# RBAC ADMIN CONFIG
# -----------------------------

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'description')
    search_fields = ('role_name',)

@admin.register(SecureRecord)
class SecureRecordAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at")
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission')
    list_filter = ('role', 'permission')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)


# -----------------------------
# QUERY LOGGING & ML ADMIN
# -----------------------------

@admin.register(SQLQueryLog)
class SQLQueryLogAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'query_type',
        'is_allowed_by_rbac',
        'is_malicious_ml',
        'final_decision',
        'timestamp'
    )

    list_filter = (
        'query_type',
        'is_allowed_by_rbac',
        'is_malicious_ml',
        'final_decision'
    )

    search_fields = (
        'user__username',
        'query_text',
    )

    readonly_fields = (
        'query_text',
        'query_type',
        'is_allowed_by_rbac',
        'is_malicious_ml',
        'final_decision',
        'timestamp'
    )


@admin.register(MLDetectionResult)
class MLDetectionResultAdmin(admin.ModelAdmin):
    list_display = (
        'query_log',
        'prediction',
        'confidence_score',
        'model_version',
        'detected_at'
    )

    list_filter = ('prediction', 'model_version')
    readonly_fields = ('detected_at',)

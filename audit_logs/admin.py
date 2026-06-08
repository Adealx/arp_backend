from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'action',
        'module',
        'created_at'
    )

    readonly_fields = (
        'user',
        'action',
        'module',
        'description',
        'created_at'
    )

    ordering = ('-created_at',)
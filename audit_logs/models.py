# audit_logs/models.py

from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    action = models.CharField(
        max_length=50
    )

    module = models.CharField(
        max_length=50
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user} - {self.action}"
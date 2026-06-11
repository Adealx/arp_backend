from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=200)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=20, blank=True, default='')

    address = models.TextField(blank=True, default='')

    company = models.CharField(max_length=200, blank=True, default='')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customers',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

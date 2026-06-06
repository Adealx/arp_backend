from django.db import models
from django.utils import timezone


class Product(models.Model):

    STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
    ]

    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    supplier = models.CharField(max_length=255)
    stock = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    last_restocked = models.DateField(default=timezone.now)
    batch_number = models.CharField(max_length=100, blank=True, default='')
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def status(self):
        if self.stock == 0:
            return 'out_of_stock'
        if self.stock <= self.reorder_level:
            return 'low_stock'
        return 'in_stock'

    def __str__(self):
        return f"{self.sku} - {self.name}"

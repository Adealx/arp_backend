from django.db import models
from django.contrib.auth.models import User


class SalesOrder(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    sales_rep = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sales_orders'
    )

    customer_name = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=100, blank=True, default='')

    # Top-level fields kept for backward compat; derived from first item
    product_name = models.CharField(max_length=255, blank=True, default='')
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, default=0)

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    due_date = models.DateField(null=True, blank=True)
    shipping_address = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_name} - {self.product_name}"


class SalesOrderItem(models.Model):
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"

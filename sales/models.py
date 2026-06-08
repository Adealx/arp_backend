from django.db import models
from django.contrib.auth.models import User

from customers.models import Customer
from products.models import Product


class SalesOrder(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Invoiced", "Invoiced"),
    ]

    sales_rep = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sales_orders"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="sales_orders"
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def update_total(self):

        total = sum(
            item.line_total
            for item in self.items.all()
        )

        self.total_amount = total

        self.save(
            update_fields=["total_amount"]
        )

    def __str__(self):

        return (
            f"Order #{self.id} - "
            f"{self.customer.name}"
        )


class SalesOrderItem(models.Model):

    order = models.ForeignKey(
        SalesOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items"
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def save(self, *args, **kwargs):

        self.line_total = (
            self.quantity *
            self.unit_price
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"Order #{self.order.id} - "
            f"{self.product.name}"
        )
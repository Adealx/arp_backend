from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from customers.models import Customer
from products.models import Product


class Invoice(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Partially Paid', 'Partially Paid'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    invoice_number = models.CharField(
        max_length=100,
        unique=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='invoices',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.invoice_number

    @property
    def total_paid(self):
        return sum(
            payment.amount_paid
            for payment in self.payments.all()
        )

    @property
    def balance_due(self):
        return self.amount - self.total_paid

    def update_status(self):

        total_paid = self.total_paid

        if total_paid <= 0 and self.due_date < timezone.now().date():
            self.status = 'Overdue'

        elif total_paid <= 0:
            self.status = 'Pending'

        elif total_paid < self.amount:
            self.status = 'Partially Paid'

        else:
            self.status = 'Paid'

        self.save()


class InvoiceItem(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def save(self, *args, **kwargs):

        self.total_price = self.quantity * self.unit_price

        super().save(*args, **kwargs)

        total = sum(
            item.total_price
            for item in self.invoice.items.all()
        )

        self.invoice.amount = total
        self.invoice.save()

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.product.name}"
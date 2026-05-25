from django.db import models
from customers.models import Customer


class Invoice(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
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
        decimal_places=2
    )

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.invoice_number

    def total_paid(self):
        return sum(
            payment.amount_paid
            for payment in self.payments.all()
        )

    def balance_due(self):
        return self.amount - self.total_paid()

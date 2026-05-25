from django.db import models
from invoices.models import Invoice


class Payment(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField()

    reference_number = models.CharField(
        max_length=100,
        unique=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.reference_number

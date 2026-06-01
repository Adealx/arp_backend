from django.db import models
from django.contrib.auth.models import User
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

    payment_date = models.DateField(
        auto_now_add=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        self.invoice.refresh_from_db()
        self.invoice.update_status()

    def __str__(self):
        return f"{self.invoice.invoice_number} - ₦{self.amount_paid}"
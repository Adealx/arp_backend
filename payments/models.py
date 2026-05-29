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

    payment_date = models.DateField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        # IMPORTANT: refresh invoice status after payment
        self.invoice.refresh_from_db()
        self.invoice.update_status()

    def __str__(self):
        return f"{self.invoice.invoice_number} - ₦{self.amount_paid}"

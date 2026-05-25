from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'reference_number',
        'invoice',
        'amount_paid',
        'payment_date',
    )

    search_fields = (
        'reference_number',
        'invoice__invoice_number',
    )

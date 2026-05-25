from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number',
        'customer',
        'amount',
        'due_date',
        'status',
    )

    search_fields = (
        'invoice_number',
        'customer__name',
    )

from django.contrib import admin
from .models import Invoice


from django.contrib import admin
from .models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = [
        'invoice_number',
        'customer',
        'amount',
        'status',
        'due_date',
        'created_at'
    ]

    readonly_fields = ['amount']

    inlines = [InvoiceItemInline]

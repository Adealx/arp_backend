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

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        user = request.user

        # Super Admin sees all
        if user.is_superuser:
            return qs

        # Admin sees all
        if user.groups.filter(name='Admin').exists():
            return qs

        # Sales Head sees all
        if user.groups.filter(name='Sales Head').exists():
            return qs

        # Sales Rep sees only own invoices
        return qs.filter(created_by=user)
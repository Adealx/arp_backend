from rest_framework import serializers
from .models import Customer
from invoices.models import Invoice


class CustomerInvoiceSerializer(serializers.ModelSerializer):

    balance_due = serializers.ReadOnlyField()

    class Meta:
        model = Invoice
        fields = [
            'id',
            'invoice_number',
            'amount',
            'status',
            'balance_due',
        ]


class CustomerSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    invoices = CustomerInvoiceSerializer(many=True, read_only=True)
    total_invoiced = serializers.SerializerMethodField()
    total_paid = serializers.SerializerMethodField()
    outstanding_balance = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'address',
            'company',
            'status',
            'created_by',
            'created_by_name',
            'created_at',
            'invoices',
            'total_invoiced',
            'total_paid',
            'outstanding_balance',
        ]
        read_only_fields = ['created_by', 'created_by_name', 'created_at']

    def get_total_invoiced(self, obj):
        return sum(invoice.amount for invoice in obj.invoices.all())

    def get_total_paid(self, obj):
        return sum(invoice.total_paid for invoice in obj.invoices.all())

    def get_outstanding_balance(self, obj):
        return sum(invoice.balance_due for invoice in obj.invoices.all())

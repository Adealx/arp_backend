from rest_framework import serializers
from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source='customer.name',
        read_only=True
    )

    total_paid = serializers.ReadOnlyField()

    balance_due = serializers.ReadOnlyField()

    class Meta:
        model = Invoice
        fields = [
            'id',
            'invoice_number',
            'customer',
            'customer_name',
            'amount',
            'due_date',
            'status',
            'created_at',
            'created_by',
            'total_paid',
            'balance_due',
        ]
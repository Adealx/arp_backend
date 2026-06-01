from rest_framework import serializers
from .models import SalesOrder


class SalesOrderSerializer(serializers.ModelSerializer):

    sales_rep_name = serializers.CharField(
        source='sales_rep.username',
        read_only=True
    )

    class Meta:
        model = SalesOrder

        fields = [
            'id',
            'sales_rep_name',
            'customer_name',
            'product_name',
            'quantity',
            'unit_price',
            'total_amount',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'total_amount',
            'created_at',
            'updated_at',
            'sales_rep_name',
        ]

from rest_framework import serializers
from .models import SalesOrder


class SalesOrderSerializer(serializers.ModelSerializer):

    sales_rep_name = serializers.CharField(
        source='sales_rep.username',
        read_only=True
    )

    class Meta:
        model = SalesOrder
        fields = '__all__'
        read_only_fields = ['sales_rep', 'total_amount', 'created_at', 'updated_at']
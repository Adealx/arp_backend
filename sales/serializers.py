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
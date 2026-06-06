from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'name',
            'category',
            'supplier',
            'stock',
            'reorder_level',
            'unit_price',
            'last_restocked',
            'batch_number',
            'expiry_date',
            'status',
            'created_at',
        ]
        read_only_fields = ['status', 'created_at']

    def get_status(self, obj):
        return obj.status

from rest_framework import serializers
from .models import SalesOrder, SalesOrderItem


class SalesOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderItem
        fields = ['id', 'product_name', 'quantity', 'unit_price']


class SalesOrderSerializer(serializers.ModelSerializer):
    sales_rep_name = serializers.CharField(source='sales_rep.username', read_only=True)
    items = SalesOrderItemSerializer(many=True, required=False)

    class Meta:
        model = SalesOrder
        fields = [
            'id',
            'sales_rep_name',
            'customer_name',
            'customer_id',
            'product_name',
            'quantity',
            'unit_price',
            'total_amount',
            'priority',
            'status',
            'due_date',
            'shipping_address',
            'notes',
            'items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['total_amount', 'created_at', 'updated_at', 'sales_rep_name']

    def _sync_items(self, order, items_data):
        order.items.all().delete()
        total = 0
        for item_data in items_data:
            item = SalesOrderItem.objects.create(order=order, **item_data)
            total += item.quantity * item.unit_price
        return total

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])

        if items_data and not validated_data.get('product_name'):
            first = items_data[0]
            validated_data['product_name'] = first['product_name']
            validated_data['quantity'] = sum(i['quantity'] for i in items_data)
            validated_data['unit_price'] = first['unit_price']

        order = SalesOrder.objects.create(**validated_data)

        if items_data:
            order.total_amount = self._sync_items(order, items_data)
        else:
            order.total_amount = order.quantity * order.unit_price

        order.save(update_fields=['total_amount'])
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if items_data is not None:
            total = self._sync_items(instance, items_data)
            instance.total_amount = total
            if items_data:
                first = items_data[0]
                instance.product_name = first['product_name']
                instance.quantity = sum(i['quantity'] for i in items_data)
                instance.unit_price = first['unit_price']

        instance.save()
        return instance

from rest_framework import serializers

from .models import (
    SalesOrder,
    SalesOrderItem
)


class SalesOrderItemSerializer(
    serializers.ModelSerializer
):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:

        model = SalesOrderItem

        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "line_total",
        ]

        read_only_fields = [
            "line_total",
            "product_name",
        ]


class SalesOrderSerializer(
    serializers.ModelSerializer
):

    sales_rep_name = serializers.CharField(
        source="sales_rep.username",
        read_only=True
    )

    customer_name = serializers.CharField(
        source="customer.name",
        read_only=True
    )

    items = SalesOrderItemSerializer(
        many=True,
        required=False
    )

    class Meta:

        model = SalesOrder

        fields = [
            "id",
            "sales_rep_name",
            "customer",
            "customer_name",
            "status",
            "total_amount",
            "items",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "sales_rep_name",
            "customer_name",
            "total_amount",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):

        items_data = validated_data.pop(
            "items",
            []
        )

        order = SalesOrder.objects.create(
            **validated_data
        )

        total = 0

        for item_data in items_data:

            item = SalesOrderItem.objects.create(
                order=order,
                **item_data
            )

            total += item.line_total

        order.total_amount = total

        order.save()

        return order

    def update(
        self,
        instance,
        validated_data
    ):

        items_data = validated_data.pop(
            "items",
            None
        )

        instance.customer = (
            validated_data.get(
                "customer",
                instance.customer
            )
        )

        instance.status = (
            validated_data.get(
                "status",
                instance.status
            )
        )

        instance.save()

        if items_data is not None:

            instance.items.all().delete()

            total = 0

            for item_data in items_data:

                item = SalesOrderItem.objects.create(
                    order=instance,
                    **item_data
                )

                total += item.line_total

            instance.total_amount = total

            instance.save()

        return instance
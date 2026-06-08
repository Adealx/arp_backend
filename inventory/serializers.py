from rest_framework import serializers

from .models import StockMovement


class StockMovementSerializer(
    serializers.ModelSerializer
):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    user_name = serializers.CharField(
        source="created_by.username",
        read_only=True
    )

    class Meta:

        model = StockMovement

        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "movement_type",
            "user_name",
            "created_at",
        ]
from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class StockMovement(models.Model):

    MOVEMENT_TYPES = [
        ("IN", "IN"),
        ("OUT", "OUT"),
        ("ADJUSTMENT", "ADJUSTMENT"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stock_movements"
    )

    quantity = models.IntegerField()

    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPES
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.product.name} "
            f"{self.movement_type} "
            f"{self.quantity}"
        )
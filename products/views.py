from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from inventory.models import StockMovement

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all().order_by(
        "name"
    )

    serializer_class = ProductSerializer

    permission_classes = [
        IsAuthenticated
    ]

    @action(
        detail=True,
        methods=["post"]
    )
    def restock(
        self,
        request,
        pk=None
    ):

        product = self.get_object()

        quantity = int(
            request.data.get(
                "quantity",
                0
            )
        )

        if quantity <= 0:

            return Response(
                {
                    "error":
                    "Quantity must be greater than zero."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        product.stock_quantity += quantity

        product.save()

        StockMovement.objects.create(
            product=product,
            quantity=quantity,
            movement_type="IN",
            created_by=request.user
        )

        return Response(
            {
                "message":
                "Product restocked successfully",
                "new_stock":
                product.stock_quantity
            }
        )
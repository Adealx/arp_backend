from datetime import date
from inventory.models import StockMovement

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from invoices.models import Invoice
from products.models import Product

from .models import (
    SalesOrder,
    SalesOrderItem,
)
from .serializers import SalesOrderSerializer


class SalesOrderViewSet(viewsets.ModelViewSet):

    queryset = SalesOrder.objects.all()

    serializer_class = SalesOrderSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        if user.profile.role in [
            "admin",
            "manager",
        ]:

            return SalesOrder.objects.all().order_by(
                "-created_at"
            )

        return SalesOrder.objects.filter(
            sales_rep=user
        ).order_by(
            "-created_at"
        )

    def perform_create(self, serializer):  

        print(self.request.data)
        
        order = serializer.save(
            sales_rep=self.request.user
        )

        items = self.request.data.get(
            "items",
            []
        )

        grand_total = 0

        for item in items:

            product_id = item.get(
                "product"
            )

            quantity = int(
                item.get(
                    "quantity",
                    0
                )
            )

            try:

                product = Product.objects.get(
                    id=product_id
                )

            except Product.DoesNotExist:

                raise ValidationError(
                    {
                        "product":
                        f"Product {product_id} not found."
                    }
                )

            if product.stock_quantity < quantity:

                raise ValidationError(
                    {
                        "quantity":
                        (
                            f"Only "
                            f"{product.stock_quantity} "
                            f"units of "
                            f"{product.name} "
                            f"available."
                        )
                    }
                )

            line_total = (
                quantity *
                product.retail_price
            )

            SalesOrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.retail_price,
                line_total=line_total,
            )

            product.stock_quantity -= quantity

            product.save()

            StockMovement.objects.create(
                product=product,
                quantity=quantity,
                movement_type="OUT",
                created_by=self.request.user
            )

            grand_total += line_total

        order.total_amount = grand_total

        order.save()

        return order


@api_view(["POST"])
def approve_order(request, pk):

    order = SalesOrder.objects.get(
        pk=pk
    )

    if request.user.profile.role not in [
        "admin",
        "manager",
    ]:

        return Response(
            {
                "error":
                "Permission denied"
            },
            status=status.HTTP_403_FORBIDDEN
        )

    order.status = "Approved"

    order.save()

    return Response(
        {
            "message":
            "Order approved"
        }
    )


@api_view(["POST"])
def convert_order_to_invoice(
    request,
    pk
):

    order = SalesOrder.objects.get(
        pk=pk
    )

    if order.status != "Approved":

        return Response(
            {
                "error":
                "Order must be approved first"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    invoice = Invoice.objects.create(
        customer=order.customer,
        invoice_number=f"INV-{order.id}",
        amount=order.total_amount,
        due_date=date.today(),
        created_by=request.user,
    )

    order.status = "Invoiced"

    order.save()

    return Response(
        {
            "invoice_id":
            invoice.id,
            "message":
            "Invoice created successfully"
        }
    )
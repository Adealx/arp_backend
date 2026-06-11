from datetime import date
from inventory.models import StockMovement

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
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


def _is_admin(user):
    return (
        user.is_superuser
        or user.groups.filter(name__in=['Admin', 'Sales Head']).exists()
        or getattr(getattr(user, 'profile', None), 'role', '') in ('admin', 'manager')
    )


class SalesOrderViewSet(viewsets.ModelViewSet):

    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        if _is_admin(user):
            return SalesOrder.objects.all().order_by('-created_at')

        return SalesOrder.objects.filter(
            sales_rep=user
        ).order_by("-created_at")

    def perform_create(self, serializer):

        order = serializer.save(sales_rep=self.request.user)

        items = self.request.data.get("items", [])
        grand_total = 0

        for item in items:

            product_id = item.get("product")
            quantity = int(item.get("quantity", 0))

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise ValidationError({"product": f"Product {product_id} not found."})

            if product.stock_quantity < quantity:
                raise ValidationError({
                    "quantity": (
                        f"Only {product.stock_quantity} units of "
                        f"{product.name} available."
                    )
                })

            line_total = quantity * product.retail_price

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

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if not _is_admin(request.user):
            return Response(
                {'error': 'Only admins can approve sales orders.'},
                status=status.HTTP_403_FORBIDDEN
            )
        order = self.get_object()
        if order.status != 'Pending':
            return Response(
                {'error': f'Cannot approve an order with status "{order.status}".'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = 'Approved'
        order.save(update_fields=['status'])
        return Response(SalesOrderSerializer(order).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        if not _is_admin(request.user):
            return Response(
                {'error': 'Only admins can reject sales orders.'},
                status=status.HTTP_403_FORBIDDEN
            )
        order = self.get_object()
        if order.status not in ('Pending', 'Approved'):
            return Response(
                {'error': f'Cannot reject an order with status "{order.status}".'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = 'Rejected'
        order.save(update_fields=['status'])
        return Response(SalesOrderSerializer(order).data)


@api_view(["POST"])
def approve_order(request, pk):

    order = SalesOrder.objects.get(pk=pk)

    if not _is_admin(request.user):
        return Response(
            {"error": "Permission denied"},
            status=status.HTTP_403_FORBIDDEN
        )

    order.status = "Approved"
    order.save()

    return Response({"message": "Order approved"})


@api_view(["POST"])
def convert_order_to_invoice(request, pk):

    order = SalesOrder.objects.get(pk=pk)

    if order.status != "Approved":
        return Response(
            {"error": "Order must be approved first"},
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

    return Response({
        "invoice_id": invoice.id,
        "message": "Invoice created successfully"
    })

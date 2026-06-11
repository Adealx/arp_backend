from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import SalesOrder
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
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(sales_rep=self.request.user)

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
        order.status = 'Pending'
        order.save(update_fields=['status'])
        return Response(SalesOrderSerializer(order).data)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import SalesOrder
from .serializers import SalesOrderSerializer


class SalesOrderViewSet(viewsets.ModelViewSet):

    queryset = SalesOrder.objects.all()

    serializer_class = SalesOrderSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Super Admin sees all sales
        if user.is_superuser:
            return SalesOrder.objects.all().order_by('-created_at')

        # Admin sees all sales
        if user.groups.filter(name='Admin').exists():
            return SalesOrder.objects.all().order_by('-created_at')

        # Sales Head sees all sales
        if user.groups.filter(name='Sales Head').exists():
            return SalesOrder.objects.all().order_by('-created_at')

        # Sales Reps see only their own sales
        return SalesOrder.objects.filter(
            sales_rep=user
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(
            sales_rep=self.request.user
        )

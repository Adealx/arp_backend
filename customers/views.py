from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Customer
from .serializers import CustomerSerializer


def _is_admin(user):
    return (
        user.is_superuser
        or user.groups.filter(name__in=['Admin', 'Sales Head']).exists()
        or getattr(getattr(user, 'profile', None), 'role', '') in ('admin', 'manager')
    )


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Customer.objects.all().order_by('-created_at')
        if not _is_admin(user):
            qs = qs.filter(created_by=user)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name__icontains=search) | Customer.objects.filter(company__icontains=search)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

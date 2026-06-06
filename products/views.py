from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Product.objects.all().order_by('-created_at')
        search = self.request.query_params.get('search')
        category = self.request.query_params.get('category')
        if search:
            qs = qs.filter(name__icontains=search) | qs.filter(sku__icontains=search)
        if category:
            qs = qs.filter(category=category)
        return qs

    @action(detail=True, methods=['post'])
    def restock(self, request, pk=None):
        product = self.get_object()
        qty = request.data.get('quantity')
        if qty is None or int(qty) <= 0:
            return Response(
                {'error': 'Provide a positive quantity'},
                status=status.HTTP_400_BAD_REQUEST
            )
        product.stock += int(qty)
        product.last_restocked = timezone.now().date()
        product.save(update_fields=['stock', 'last_restocked'])
        return Response(ProductSerializer(product).data)

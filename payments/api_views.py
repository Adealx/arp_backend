from rest_framework import generics
from .models import Payment
from .serializers import PaymentSerializer


class PaymentListAPIView(generics.ListCreateAPIView):
    queryset = Payment.objects.all().order_by('-payment_date')
    serializer_class = PaymentSerializer
from django.urls import path
from .api_views import PaymentListAPIView

urlpatterns = [
    path('', PaymentListAPIView.as_view(), name='payment-list'),
]
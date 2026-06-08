from django.urls import path
from .views import (
    invoice_api,
    invoice_detail_api,
)

urlpatterns = [
    path('', invoice_api),
    path('<int:pk>/', invoice_detail_api),
]
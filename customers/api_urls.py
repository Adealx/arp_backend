from django.urls import path
from .views import (
    customer_api,
    customer_detail_api,
)

urlpatterns = [
    path('', customer_api),
    path('<int:pk>/', customer_detail_api),
]
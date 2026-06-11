from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    SalesOrderViewSet,
    approve_order,
    convert_order_to_invoice,
)

router = DefaultRouter()

router.register(
    r'',
    SalesOrderViewSet,
    basename='orders'
)

urlpatterns = [

    path('', include(router.urls)),

    path('<int:pk>/approve/', approve_order),

    path('<int:pk>/invoice/', convert_order_to_invoice),

]

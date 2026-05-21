from django.urls import path

from .views import (
    get_orders,
    create_order,
    single_order,
    update_order,
    delete_order,
    dashboard_stats
)

urlpatterns = [

    path('orders/', get_orders, name='get_orders'),

    path('create/', create_order, name='create_order'),

    path('order/<int:pk>/', single_order, name='single_order'),

    path('update/<int:pk>/', update_order, name='update_order'),

    path('delete/<int:pk>/', delete_order, name='delete_order'),

    path('dashboard/stats/', dashboard_stats),

]
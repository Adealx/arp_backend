from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),

    path('api/', include('sales.urls')),

    path('customers/', include('customers.urls')),

    path('invoices/', include('invoices.urls')),

    path('payments/', include('payments.urls')),

    path('inventory/', include('products.urls')),
]

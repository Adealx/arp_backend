from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth (login, register, me)
    path('accounts/', include('accounts.urls')),

    # Sales orders REST API
    path('api/', include('sales.urls')),

    # Customers REST API
    path('api/customers/', include('customers.urls')),

    # Inventory / Products REST API
    path('inventory/', include('products.urls')),

    # Dashboard stats REST API
    path('api/dashboard/', include('dashboard.urls')),

    # Invoices & payments (template views)
    path('invoices/', include('invoices.urls')),
    path('payments/', include('payments.urls')),
]

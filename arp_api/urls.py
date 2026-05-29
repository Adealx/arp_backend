from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('sales.urls')),

    path('customers/', include('customers.urls')),

    path('invoices/', include('invoices.urls')),

    path('payments/', include('payments.urls')),
]

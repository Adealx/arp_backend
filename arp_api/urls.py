from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "api/accounts/",
        include("accounts.api_urls")
    ),

    path(
        "api/customers/",
        include("customers.api_urls")
    ),

    path(
        "api/products/",
        include("products.api_urls")
    ),

    path(
        "api/invoices/",
        include("invoices.api_urls")
    ),

    path(
        "api/payments/",
        include("payments.api_urls")
    ),

    path(
        "api/orders/",
        include("sales.api_urls")
    ),

    path(
        "api/stock-movements/",
        include("inventory.api_urls")
    ),

]

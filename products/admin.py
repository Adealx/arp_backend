from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'sku',
        'name',
        'category',
        'supplier',
        'stock',
        'reorder_level',
        'unit_price',
        'status',
        'last_restocked',
        'created_at',
    ]


admin.site.register(Product, ProductAdmin)

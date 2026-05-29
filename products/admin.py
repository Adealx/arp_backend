from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'sku',
        'name',
        'retail_price',
        'wholesale_price',
        'stock_quantity',
        'created_at',
    ]


admin.site.register(Product, ProductAdmin)

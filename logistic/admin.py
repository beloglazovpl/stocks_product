from django.contrib import admin

from logistic.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'address']


@admin.register(StockProduct)
class StockProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'stock_id', 'product_id', 'quantity', 'price']

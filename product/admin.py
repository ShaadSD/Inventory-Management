from django.contrib import admin
from .models import Category, Product, Customer, SalesRecord, StockMovement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'quantity', 'price','supplier')
    list_filter = ('category',)
    search_fields = ('name', 'sku')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_sold', 'date', 'customer', 'sold_by')
    list_filter = ('date', 'sold_by')
    search_fields = ('product__name', 'customer__name')


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'movement_type', 'reason', 'date', 'actioned_by')
    list_filter = ('movement_type', 'date')
    search_fields = ('product__name', 'reason')
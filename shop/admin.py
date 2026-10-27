
from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "stock")
    search_fields = ("name",)

from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "price", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "phone",
        "total_amount",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "email", "phone")
    readonly_fields = ("created_at", "total_amount")
    inlines = [OrderItemInline]

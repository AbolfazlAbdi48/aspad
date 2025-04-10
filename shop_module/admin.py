from django.contrib import admin

from shop_module.models import Product, Order, OrderDetail, Shop


# Register your models here.
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderDetailInline
    ]

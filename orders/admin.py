
from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("subtotal",)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "customer_name",
        "total_amount",
        "status",
        "created_at",
    )
    inlines = [OrderItemInline]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
        "subtotal",
    )
    list_select_related = ("order", "product")


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

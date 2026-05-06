from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'sku', 'price', 'quantity', 'subtotal')

    def subtotal(self, obj):
        return f"₹{obj.subtotal}"
    subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('short_uuid', 'customer', 'total_amount', 'order_status', 'created_at')
    list_filter   = ('order_status',)
    search_fields = ('customer__username', 'shipping_name')
    readonly_fields = ('order_uuid', 'created_at', 'updated_at')
    inlines       = [OrderItemInline]

    def short_uuid(self, obj):
        return obj.short_uuid
    short_uuid.short_description = 'Order ID'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'sku', 'price', 'quantity')

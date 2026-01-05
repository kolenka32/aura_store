from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product', 'size', 'quantity', 'price', 'get_total']
    readonly_fields = ['get_total']
    autocomplete_fields = ['product', 'size']

    def get_total(self, obj):
        return f"{obj.get_total_price()} руб."

    get_total.short_description = 'Сумма'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_name', 'email', 'phone', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'items_list']
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'status', 'payment_provider', 'total_price')
        }),
        ('Данные покупателя', {
            'fields': (('first_name', 'last_name'), 'email', 'phone', 'address')
        }),
        ('Товары в заказе', {
            'fields': ('items_list',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [OrderItemInline]

    def short_name(self, obj):
        return f"{obj.first_name} {obj.last_name[0]}." if obj.last_name else obj.first_name

    short_name.short_description = 'Имя'

    def items_list(self, obj):
        items = obj.items.all()
        if not items:
            return "Нет товаров"

        text = "\n".join([
            f"• {item.product.name} ({item.size.name}): {item.quantity} × {item.price} руб. = {item.get_total_price()} руб."
            for item in items
        ])
        return format_html('<pre style="background: #f5f5f5; padding: 10px;">{}</pre>', text)

    items_list.short_description = 'Состав заказа'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'product_name', 'size', 'quantity', 'price', 'total']
    list_filter = ['order__status']
    search_fields = ['product__name', 'order__first_name', 'order__last_name']

    def order_id(self, obj):
        return f"#{obj.order.id}"

    order_id.short_description = 'Заказ'

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = 'Товар'

    def total(self, obj):
        return f"{obj.get_total_price()} руб."

    total.short_description = 'Сумма'
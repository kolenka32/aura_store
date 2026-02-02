from django.contrib import admin
from django.utils.html import format_html

from .models import CartItem, Cart

# Register your models here.
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ['added_at', 'total_price']



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','session_key_display', 'created_at', 'updated_at', 'total_items', 'subtotal']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['session_key']
    readonly_fields = ['total_items', 'subtotal']
    inlines = [CartItemInline]

    def session_key_display(self, obj):
        if obj.session_key:
            return format_html(f'<span style="color: green;">{obj.session_key}</span>')
        return format_html(f'<span style="color: green;">Корзина пользователя: <b>{obj.user}</b></span>')

    session_key_display.short_description = 'Session key'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'product_size', 'quantity', 'added_at', 'total_price']
    list_filter = ['cart', 'product_size']
    search_fields = ['product__name', 'cart_session_key']

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from cart.models import Cart, CartItem


class CartInline(admin.StackedInline):
    model = Cart
    extra = 0
    show_change_link = True


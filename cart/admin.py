from django.contrib import admin
from .models import CartItem, Cart

# Register your models here.
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ['added_at', 'total_price']



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'created_at', 'updated_at', 'total_items', 'subtotal']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['session_key']
    readonly_fields = ['total_items', 'subtotal']
    inlines = [CartItemInline]



@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'product_size', 'quantity', 'added_at', 'total_price']
    list_filter = ['cart', 'product_size']
    search_fields = ['product__name', 'cart_session_key']


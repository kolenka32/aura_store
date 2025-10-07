from django.contrib import admin
from .models import Category, Product, Color, Size, ProductSize, ProductImage




# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['color']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProcuctAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'color', 'created_at', 'updated_at']
    search_fields = ['name', 'category', 'color', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', 'color']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductSizeInline, ProductImageInline]
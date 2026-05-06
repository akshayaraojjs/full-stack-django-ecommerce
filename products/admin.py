from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'sku_prefix', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'product_name', 'seller', 'category', 'price', 'stock', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('product_name', 'sku', 'seller__username')
    readonly_fields = ('sku',)
    inlines = [ProductImageInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'uploaded_at')

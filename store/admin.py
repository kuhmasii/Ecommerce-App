from django.contrib import admin
from . models import Product, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = "name slug".split()
    prepopulated_fields = {"slug": ("name",)}


class ProductAdmin(admin.ModelAdmin):
    list_display = "name slug price available created updated".split()
    list_filter = "available created updated".split()
    list_editable = "available price".split()
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

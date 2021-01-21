from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
        model = OrderItem
        raw_id_field = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = "first_name last_name email address country city created paid".split()
    list_filter = "paid country city created updated".split()
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)

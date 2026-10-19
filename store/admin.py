from django.contrib import admin
from .models import Category, Product, Order, OrderItem


admin.site.register(Category)
admin.site.register(Product)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'phone', 'city',
                    'total', 'payment_method', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('full_name', 'phone', 'user__username')
    inlines = [OrderItemInline]

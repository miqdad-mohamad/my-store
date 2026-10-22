from django.contrib import admin
from .models import Category, Product, Order, OrderItem,UserProfile


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserProfile)



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'phone', 'city',
                    'get_items', 'total', 'payment_method', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('full_name', 'phone', 'user__username')
    list_editable = ('status',)
    inlines = [OrderItemInline]

    def get_items(self, obj):
        items = obj.items.all()
        return ", ".join([f"{item.product.name} (x{item.quantity})" for item in items])

    get_items.short_description = 'Items Ordered'

from django.contrib import admin
from .models import Product, Cart, Orders

# Register your models here.

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_price', 'status')
    list_filter = ('status',)
    actions = ['confirm_orders', 'cancel_orders']

    def confirm_orders(self, request, queryset):
        queryset.update(status='Delivered')
        self.message_user(request, "Đã xác nhận đơn hàng.")
    confirm_orders.short_description = "Xác nhận đơn hàng"

    def cancel_orders(self, request, queryset):
        queryset.update(status='Cancelled')
        self.message_user(request, "Đã hủy đơn hàng.")
    cancel_orders.short_description = "Hủy đơn hàng"

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Orders, OrdersAdmin)

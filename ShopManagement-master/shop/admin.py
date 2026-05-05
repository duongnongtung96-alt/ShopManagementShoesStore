from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.models import User
from products.models import Orders, OrderDetails

class CustomAdminSite(admin.AdminSite):
    site_header = "Shop Management Admin"
    site_title = "Shop Admin"
    index_title = "Welcome to Shop Admin"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        total_orders = Orders.objects.count()
        total_revenue = Orders.objects.filter(status='Delivered').aggregate(Sum('total_price'))['total_price__sum'] or 0
        total_products_sold = OrderDetails.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_users = User.objects.count()
        extra_context.update({
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_products_sold': total_products_sold,
            'total_users': total_users,
        })
        return super().index(request, extra_context)

admin.site = CustomAdminSite()
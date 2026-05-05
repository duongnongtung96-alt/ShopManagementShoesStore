from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.product_search, name='product_search'),
    path('cart/', views.cart_get, name='cart_get'),
    path('orders/', views.orders_get, name='orders_get'),
    path('viewproduct/<str:pid>/', views.product_details, name='product_details'),
    path('order_from_cart/', views.order_from_cart, name='order_from_cart'),
    path('cart/delete/<str:pid>/', views.cart_delete, name="cart_delete"),
    path('orders/details/<str:oid>', views.order_details, name='order_details'),
    path('orders/update_payment/<str:oid>/', views.update_payment, name='update_payment'),
    path('orders/confirm/<str:oid>', views.order_confirm, name='order_confirm'),
    path('orders/cancel/<str:oid>', views.order_cancel, name='order_cancel'),
    path('order/<str:pid>/', views.order_product, name='order_product'),
    path('buy_now/<str:pid>/', views.buy_now, name='buy_now'),
    path('reports/', views.reports, name='reports'),
    # Fk that, stay here!
    path('<str:pid>/', views.cart_add, name='cart'),
]

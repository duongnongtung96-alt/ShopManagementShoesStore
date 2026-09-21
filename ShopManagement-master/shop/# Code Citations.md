# Code Citations

## License: unknown
https://github.com/ichirou2910/ShopManagement/blob/93c20f7d8a6ce66191ff7f84d77b5d4929b27b15/products/models.py

```
.Model):
    order_id = models.AutoField(db_column='order_id', primary_key=True)
    user = models.CharField(db_column='user', default='noname', max_length=25)
    customer_name = models.CharField(db_column='customer_name', default='noname', max_length=25)
    address = models.CharField(db_column='address', default='nonexistent', max_length=100)
    phone_number = models.CharField(db_column='phone_number', default='0000000000', max_length=15)
    total_price = models.IntegerField(db_column='total_price', default=0)
    status = models.CharField(db_column='status', max_length=10, default='Pending')

    class Meta:
        db_table =
```


## License: unknown
https://github.com/ichirou2910/ShopManagement/blob/93c20f7d8a6ce66191ff7f84d77b5d4929b27b15/products/urls.py

```
[
    path('', views.home, name='home'),
    path('search', views.product_search, name='product_search'),
    path('cart/', views.cart_get, name='cart_get'),
    path('orders/', views.orders_get, name='orders_get'),
    path('viewproduct/<str:pid>/', views.product_details, name='product_details'),
    path('checkout/', views.cart_checkout, name='cart_checkout'),
    path('cart/delete/<str:pid>/', views.cart_delete, name="cart_delete"),
    path('orders/details/<str:oid>', views.order_details, name='order_details'),
```


## License: unknown
https://github.com/ichirou2910/ShopManagement/blob/93c20f7d8a6ce66191ff7f84d77b5d4929b27b15/products/views.py

```
)
    else:
        name = ''
        address = ''
        phone = ''

    if name and address:
        # Create an order
        order = Orders(user=request.user.username, customer_name=name, address=address, phone_number=phone, total_price=total_price)

        # If success, create orderdetail
        if order:
            order.save()
            messages.add_message(request, messages.INFO, 'Orders accepted! Wait for your delivery!')

            for item in cart:
                # Add to order table
                order_detail = OrderDetails(order_id=order, user=item.user, quantity=item.quantity, product_id=Product.objects.get(product_id=item.product_id.product_id))
                order_detail.save()
                # Decrease quantity in stock
                # product = products.get(product_id=item.product_id.product_id)
                item.product_id.quantity_in_stock -= item.quantity
                item.product_id.save(update_fields=['quantity_in_stock'])

            # Empty your cart
            Cart.objects.filter(user=request.user.username).delete()
            return redirect('/')
        messages.add_message(request, messages.INFO, 'Oops!')

    return render(request, 'checkout.html', {
        'cart': cart,
        'total':
```


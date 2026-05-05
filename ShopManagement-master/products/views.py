"""Import models"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.utils.html import escape

from .models import Product, Cart, Orders, OrderDetails

# Create your views here.


def home(request):
    """ Render product page """
    pds = Product.objects.all().order_by('product_id')
    return render(request, 'product.html', {'products': pds, 'count': pds.count()})


def product_search(request):
    pds = Product.objects.all()

    if 'pname' in request.GET:
        pname = escape(request.GET["pname"])
        pds = pds.filter(product_name__icontains=pname)

    if 'filter' in request.GET:
        availability = escape(request.GET["filter"])
        if availability == 'avail':
            pds = pds.filter(~Q(quantity_in_stock=0))
        elif availability == 'sold-out':
            pds = pds.filter(quantity_in_stock=0)

    if 'sort' in request.GET:
        sort = escape(request.GET["sort"])
        if sort == 'name-a-to-z':
            pds = pds.order_by('product_name')
        elif sort == 'name-z-to-a':
            pds = pds.order_by('-product_name')
        elif sort == 'price-up':
            pds = pds.order_by('sell_price')
        elif sort == 'price-down':
            pds = pds.order_by('-sell_price')

    return render(request, 'product.html', {'products': pds, 'count': pds.count()})


def product_details(request, pid):
    in_cart = Cart.objects.filter(user=request.user.username, product_id=pid).values('product_id', 'user').annotate(quantity=Sum('quantity'))
    quantity = 0
    if in_cart:
        quantity = in_cart.get(product_id=pid).get('quantity')
    product = Product.objects.get(product_id=pid)
    return render(request, 'product_details.html', {'product': product, 'quantity': quantity})


def cart_add(request, pid):
    if request.user.is_superuser:
        return HttpResponse("Invalid")
    # delete old messages
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == 'POST':
        quantity = request.POST['quantity']
    else:
        quantity = 0

    if request.user.is_authenticated:
        user = request.user.username
    else:
        user = "none"

    product_get = Product.objects.get(product_id=pid)
    product_stock = product_get.quantity_in_stock

    in_cart = Cart.objects.filter(user=request.user.username, product_id__pk=pid)
    cart_quantity = 0
    if in_cart:
        cart_quantity = in_cart.get(product_id__pk=pid).quantity

    if quantity != 0 and user != "none":
        if int(quantity) + cart_quantity > product_stock:
            messages.add_message(request, messages.INFO, "Heyyyy! You know we do not have that many right?")
        else:
            messages.add_message(request, messages.INFO, 'You have added a product to your cart!')
            product_temp = Cart.objects.filter(user=request.user.username, product_id__pk=pid)
            if product_temp:
                pd_temp = product_temp.get(product_id__pk=pid)
                pd_temp.quantity = int(quantity) + cart_quantity
                pd_temp.save(update_fields=['quantity'])
            else:
                print('Product not found. Creating new.')
                product_new = Cart(product_id=Product.objects.get(product_id=pid), quantity=quantity, user=user)
                product_new.save()
    else:
        messages.add_message(request, messages.INFO, 'Oops!')

    return redirect('/products')


def cart_get(request):
    if request.user.is_superuser:
        return HttpResponse("Invalid")
    cart = Cart.objects.filter(user=request.user.username).select_related('product_id')
    stock_changed = False
    total_price = 0
    for item in cart:
        in_stock = item.product_id.quantity_in_stock
        # If empty stock, remove entry from cart
        if in_stock == 0:
            Cart.objects.filter(user=request.user.username, product_id=item.product_id).delete()
            stock_changed = True
        # Else, change the quantity of that entry in cart
        elif item.quantity > in_stock:
            Cart.objects.filter(user=request.user.username, product_id=item.product_id).update(quantity=in_stock)
            stock_changed = True

        total_price += item.product_id.sell_price * item.quantity

    return render(request, 'cart.html', {'cart': cart, 'changed': stock_changed, 'total': total_price})


def orders_get(request):
    if not request.user.is_authenticated:
        return HttpResponse("You don't have permission to view this page")

    if request.user.is_superuser:
        # Show all orders, including canceled
        orders_list = Orders.objects.order_by('-order_id')
        total_orders = orders_list.count()

        # Revenue should count only confirmed/delivered orders
        revenue_orders = orders_list.filter(status__in=['Confirmed', 'Delivered'])
        total_revenue = revenue_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

        # Products sold - count from confirmed/delivered orders only
        total_products = OrderDetails.objects.filter(order_id__in=revenue_orders.values_list('order_id', flat=True)).aggregate(Sum('quantity'))['quantity__sum'] or 0

        context = {
            'orders': orders_list,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_products': total_products,
        }
    else:
        orders_list = Orders.objects.filter(user=request.user.username).order_by('-order_id')
        context = {'orders': orders_list}

    return render(request, 'order.html', context)


def order_from_cart(request):
    if request.user.is_superuser:
        return HttpResponse("Invalid")
    # delete old messages
    storage = messages.get_messages(request)
    storage.used = True

    if request.method != 'POST':
        messages.add_message(request, messages.INFO, 'Phải gửi form đặt hàng từ giỏ hàng.')
        return redirect('/products/cart')

    selected_ids = request.POST.getlist('selected_products')
    if not selected_ids:
        messages.add_message(request, messages.INFO, 'Vui lòng chọn ít nhất một sản phẩm để đặt hàng.')
        return redirect('/products/cart')

    name = escape(request.POST.get('name', '').strip())
    phone = escape(request.POST.get('phone', '').strip())
    address = escape(request.POST.get('address', '').strip())

    if not (name and phone and address):
        messages.add_message(request, messages.INFO, 'Vui lòng nhập tên, số điện thoại và địa chỉ.')
        return redirect('/products/cart')

    cart = Cart.objects.filter(user=request.user.username, product_id__product_id__in=selected_ids).select_related('product_id')
    if not cart:
        messages.add_message(request, messages.INFO, 'Sản phẩm đã chọn không tồn tại trong giỏ hàng.')
        return redirect('/products/cart')

    total_price = 0
    for item in cart:
        total_price += item.product_id.sell_price * item.quantity

    order = Orders(
        user=request.user.username,
        customer_name=name,
        address=address,
        phone_number=phone,
        total_price=total_price,
        status='Pending',
        payment_status='Chờ thanh toán'
    )
    order.save()

    for item in cart:
        order_detail = OrderDetails(
            order_id=order,
            user=item.user,
            quantity=item.quantity,
            product_id=item.product_id
        )
        order_detail.save()
        item.product_id.quantity_in_stock -= item.quantity
        item.product_id.save(update_fields=['quantity_in_stock'])

    Cart.objects.filter(user=request.user.username, product_id__product_id__in=selected_ids).delete()

    messages.add_message(request, messages.INFO, 'Đơn hàng đã được tạo! Vui lòng thanh toán.')
    return redirect('/products/orders/details/' + str(order.order_id))


def cart_delete(request, pid):
    if request.user.is_superuser:
        return HttpResponse("Invalid")
    Cart.objects.filter(product_id__pk=pid).delete()
    return redirect('/products/cart')


def order_confirm(request, oid):
    """Allow superuser to confirm an order only after payment is completed."""
    if not request.user.is_superuser:
        return HttpResponse("Invalid")

    order = get_object_or_404(Orders, order_id=oid)
    if order.payment_status != 'Đã thanh toán':
        messages.add_message(request, messages.INFO, 'Đơn hàng chưa thanh toán nên không thể xác nhận.')
        return redirect('/products/orders/details/' + str(order.order_id))

    if order.status == 'Pending':
        order.status = 'Confirmed'
        order.save(update_fields=['status'])
    return redirect('/products/orders')


def order_cancel(request, oid):
    """Allow user to cancel their own pending order, or allow admin to cancel any order."""
    order = get_object_or_404(Orders, order_id=oid)

    if request.user.is_superuser or (request.user.is_authenticated and order.user == request.user.username):
        if order.status != 'Canceled':
            order.status = 'Canceled'
            order.save(update_fields=['status'])

            # Restore product quantity only if it was pending/confirmed
            details = OrderDetails.objects.filter(order_id=order).select_related('product_id')
            for item in details:
                item.product_id.quantity_in_stock += item.quantity
                item.product_id.save(update_fields=['quantity_in_stock'])

    return redirect('/products/orders')


def update_payment(request, oid):
    if not request.user.is_authenticated:
        return HttpResponse("Invalid")

    order = get_object_or_404(Orders, order_id=oid)

    if request.method != 'POST':
        return redirect('/products/orders/details/' + str(order.order_id))

    if request.user.is_superuser:
        return HttpResponse("Invalid", status=403)

    if not (order.user == request.user.username):
        return HttpResponse("Invalid", status=403)

    if order.status == 'Canceled':
        messages.add_message(request, messages.INFO, 'Đơn hàng đã bị hủy, không thể thanh toán.')
        return redirect('/products/orders/details/' + str(order.order_id))

    if order.payment_status != 'Chờ thanh toán':
        messages.add_message(request, messages.INFO, 'Đơn hàng đã ở trạng thái thanh toán hoặc không thể cập nhật.')
        return redirect('/products/orders/details/' + str(order.order_id))

    order.payment_status = 'Đã thanh toán'
    order.save(update_fields=['payment_status'])
    messages.add_message(request, messages.SUCCESS, 'Cập nhật thanh toán thành công.')
    return redirect('/products/orders/details/' + str(order.order_id))


def order_details(request, oid):
    if not request.user.is_authenticated:
        return HttpResponse("You don't have permission to view this page")

    if request.user.is_superuser:
        order = get_object_or_404(Orders, order_id=oid)
    else:
        order = get_object_or_404(Orders, order_id=oid, user=request.user.username)

    order_items = OrderDetails.objects.filter(order_id=order).select_related('product_id')
    total_items = order_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    # Compute per-item totals to avoid template filter issues
    items = []
    for item in order_items:
        items.append({
            'product': item.product_id,
            'quantity': item.quantity,
            'total': item.quantity * item.product_id.sell_price,
        })

    return render(request, 'order_details.html', {
        'order': order,
        'order_items': items,
        'total_items': total_items,
    })


def buy_now(request, pid):
    if request.user.is_superuser:
        return HttpResponse("Invalid")

    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Bạn cần đăng nhập để mua hàng.')
        return redirect('login')

    # delete old messages
    storage = messages.get_messages(request)
    storage.used = True

    product = get_object_or_404(Product, product_id=pid)
    if product.quantity_in_stock <= 0:
        messages.add_message(request, messages.INFO, 'Sản phẩm đã hết hàng!')
        return redirect('/products')

    payment_method = 'cash'
    quantity = 1
    if request.method == 'POST':
        name = escape(request.POST.get('name', ''))
        address = escape(request.POST.get('address', ''))
        phone = escape(request.POST.get('phone', ''))
        quantity = int(escape(request.POST.get('quantity', '1')))
        payment_method = escape(request.POST.get('payment_method', 'cash'))

        if quantity > product.quantity_in_stock:
            messages.add_message(request, messages.INFO, 'Không đủ số lượng trong kho!')
            return redirect('/products/buy_now/' + pid)

        if name and address and phone:
            total_price = product.sell_price * quantity
            # Create an order
            order = Orders(
                user=request.user.username,
                customer_name=name,
                address=address,
                phone_number=phone,
                total_price=total_price,
                status='Pending',
                payment_status='Chờ thanh toán'
            )
            order.save()

            # Create order detail
            order_detail = OrderDetails(
                order_id=order,
                user=request.user.username,
                quantity=quantity,
                product_id=product
            )
            order_detail.save()

            # Decrease stock
            product.quantity_in_stock -= quantity
            product.save(update_fields=['quantity_in_stock'])

            messages.add_message(request, messages.INFO, 'Đơn hàng đã được tạo! Vui lòng thanh toán.')
            return redirect('/products/orders/details/' + str(order.order_id))
        else:
            messages.add_message(request, messages.INFO, 'Vui lòng điền đầy đủ thông tin!')

    return render(request, 'buy_now.html', {
        'product': product,
        'quantity': quantity,
        'payment_method': payment_method,
    })


def order_product(request, pid):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, product_id=pid)
        if product.quantity_in_stock > 0:
            order = Orders.objects.create(
                user=request.user.username,
                customer_name=request.user.first_name,
                address="Default Address",
                phone_number="0000000000",
                total_price=product.sell_price,
                status="Pending"
            )
            OrderDetails.objects.create(
                order_id=order,
                user=request.user.username,
                quantity=1,
                product_id=product
            )
            product.quantity_in_stock -= 1
            product.save()
            return redirect('/products/orders/')
        else:
            return HttpResponse("Product is out of stock.")
    return HttpResponse("You need to log in to order.")


def reports(request):
    """ Generate reports for admin """
    if not request.user.is_superuser:
        return HttpResponse("Access denied.")

    total_orders = Orders.objects.count()
    total_revenue = Orders.objects.filter(status='Delivered').aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_products_sold = OrderDetails.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_users = User.objects.count()

    return render(request, 'reports.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products_sold': total_products_sold,
        'total_users': total_users,
    })

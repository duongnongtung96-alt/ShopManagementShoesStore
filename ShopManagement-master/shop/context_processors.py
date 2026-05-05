from django.db.models import Sum
from django.contrib.auth.models import User
from products.models import Orders, OrderDetails

def admin_stats(request):
    if request.user.is_superuser and request.path.startswith('/admin/'):
        total_orders = Orders.objects.count()
        total_revenue = Orders.objects.filter(status='Delivered').aggregate(Sum('total_price'))['total_price__sum'] or 0
        total_products_sold = OrderDetails.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_users = User.objects.count()
        return {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_products_sold': total_products_sold,
            'total_users': total_users,
        }
    return {}
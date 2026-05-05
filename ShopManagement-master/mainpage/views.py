from django.shortcuts import render
from products.models import Product

# Create your views here.


def home(request):
    products = Product.objects.all()[:6]  # Hiển thị 6 sản phẩm đầu tiên
    return render(request, 'index.html', {'products': products})

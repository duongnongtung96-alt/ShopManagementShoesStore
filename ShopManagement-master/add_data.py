import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from products.models import Product, Cart, Orders, OrderDetails

# Xóa dữ liệu cũ (tùy chọn)
# Product.objects.all().delete()
# Orders.objects.all().delete()
# Cart.objects.all().delete()

# Thêm dữ liệu sản phẩm test
products_data = [
    {
        'product_id': 'P001',
        'product_name': 'Laptop Dell',
        'product_image': 'laptop.jpg',
        'company': 'Dell',
        'product_description': 'Laptop Dell XPS 13 với Intel i7, RAM 16GB',
        'quantity_in_stock': 10,
        'sell_price': 15000000
    },
    {
        'product_id': 'P002',
        'product_name': 'iPhone 15',
        'product_image': 'iphone.jpg',
        'company': 'Apple',
        'product_description': 'iPhone 15 Pro Max với màn hình 6.7 inch',
        'quantity_in_stock': 20,
        'sell_price': 25000000
    },
    {
        'product_id': 'P003',
        'product_name': 'Samsung Galaxy S24',
        'product_image': 'samsung.jpg',
        'company': 'Samsung',
        'product_description': 'Samsung Galaxy S24 Ultra với camera 200MP',
        'quantity_in_stock': 15,
        'sell_price': 22000000
    },
    {
        'product_id': 'P004',
        'product_name': 'AirPods Pro',
        'product_image': 'airpods.jpg',
        'company': 'Apple',
        'product_description': 'AirPods Pro 2 với noise cancelling',
        'quantity_in_stock': 50,
        'sell_price': 6000000
    },
    {
        'product_id': 'P005',
        'product_name': 'iPad Air',
        'product_image': 'ipad.jpg',
        'company': 'Apple',
        'product_description': 'iPad Air 2024 với M2 chip',
        'quantity_in_stock': 12,
        'sell_price': 18000000
    },
]

# Thêm sản phẩm nếu chưa tồn tại
for data in products_data:
    if not Product.objects.filter(product_id=data['product_id']).exists():
        Product.objects.create(**data)
        print(f"✓ Đã thêm sản phẩm: {data['product_name']}")
    else:
        print(f"○ Sản phẩm '{data['product_name']}' đã tồn tại!")

print("\n" + "="*50)
print("✓ Thêm dữ liệu test hoàn tất!")
print("="*50)
print("\nCách truy cập:")
print("1. Django Admin: http://127.0.0.1:8000/admin/")
print("   Username: admin")
print("   Password: admin123")
print("\n2. Trang chủ shop: http://127.0.0.1:8000/")

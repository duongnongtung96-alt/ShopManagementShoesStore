import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from products.models import Product, Cart, Orders, OrderDetails

# Xóa dữ liệu sản phẩm cũ
Product.objects.all().delete()
Cart.objects.all().delete()
Orders.objects.all().delete()
OrderDetails.objects.all().delete()

print("✓ Đã xóa dữ liệu cũ!")

# Thêm dữ liệu sản phẩm giày dép
shoes_data = [
    {
        'product_id': 'S001',
        'product_name': 'Nike Air Force 1',
        'product_image': 'nike-air-force.jpg',
        'company': 'Nike',
        'product_description': 'Giày sneaker Nike Air Force 1 da trắng - kinh điển',
        'quantity_in_stock': 30,
        'sell_price': 2500000
    },
    {
        'product_id': 'S002',
        'product_name': 'Adidas Stan Smith',
        'product_image': 'adidas-stan-smith.jpg',
        'company': 'Adidas',
        'product_description': 'Giày Adidas Stan Smith trắng xanh - thể thao',
        'quantity_in_stock': 25,
        'sell_price': 2200000
    },
    {
        'product_id': 'S003',
        'product_name': 'Converse Chuck Taylor',
        'product_image': 'converse-chuck.jpg',
        'company': 'Converse',
        'product_description': 'Giày vải Converse Chuck Taylor - cổ cao',
        'quantity_in_stock': 35,
        'sell_price': 1800000
    },
    {
        'product_id': 'S004',
        'product_name': 'New Balance 990v6',
        'product_image': 'new-balance-990.jpg',
        'company': 'New Balance',
        'product_description': 'Giày chạy New Balance 990v6 - êm chân cao cấp',
        'quantity_in_stock': 20,
        'sell_price': 3500000
    },
    {
        'product_id': 'S005',
        'product_name': 'Puma RS-X',
        'product_image': 'puma-rs-x.jpg',
        'company': 'Puma',
        'product_description': 'Giày Puma RS-X đẹp mắt - năng động',
        'quantity_in_stock': 28,
        'sell_price': 2000000
    },
    {
        'product_id': 'S006',
        'product_name': 'Vans Old Skool',
        'product_image': 'vans-old-skool.jpg',
        'company': 'Vans',
        'product_description': 'Giày Vans Old Skool đen trắng - phong cách Skateboard',
        'quantity_in_stock': 32,
        'sell_price': 1950000
    },
    {
        'product_id': 'S007',
        'product_name': 'Clarks Wallabee',
        'product_image': 'clarks-wallabee.jpg',
        'company': 'Clarks',
        'product_description': 'Giày Clarks Wallabee da lộn - thoải mái ưu tiên',
        'quantity_in_stock': 18,
        'sell_price': 3200000
    },
    {
        'product_id': 'S008',
        'product_name': 'Skechers GO Walk',
        'product_image': 'skechers-go-walk.jpg',
        'company': 'Skechers',
        'product_description': 'Giày Skechers GO Walk - giày tập đi',
        'quantity_in_stock': 40,
        'sell_price': 1600000
    },
]

# Thêm sản phẩm
for data in shoes_data:
    Product.objects.create(**data)
    print(f"✓ Đã thêm: {data['product_name']}")

print("\n" + "="*60)
print("✓ SHOP GIÀY DÉP ĐÃ SẴN SÀNG!")
print("="*60)
print(f"\nTổng {len(shoes_data)} mẫu giày đã được thêm!")
print("\nCách truy cập:")
print("1. Trang chủ shop: http://127.0.0.1:8000/")
print("2. Django Admin: http://127.0.0.1:8000/admin/")
print("   Username: admin | Password: admin123")

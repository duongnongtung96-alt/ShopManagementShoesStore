import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from products.models import Product

# Xóa toàn bộ sản phẩm cũ
Product.objects.all().delete()
print("✓ Đã xóa dữ liệu cũ!\n")

# Dữ liệu 8 sản phẩm giày
shoes_data = [
    {
        'product_id': 'S001',
        'product_name': 'Nike Air Force 1',
        'product_image': 'products/s001_shoe.png',
        'company': 'Nike',
        'product_description': 'Giày sneaker Nike Air Force 1 da trắng - kinh điển',
        'quantity_in_stock': 30,
        'sell_price': 2500000
    },
    {
        'product_id': 'S002',
        'product_name': 'Adidas Stan Smith',
        'product_image': 'products/s002_shoe.png',
        'company': 'Adidas',
        'product_description': 'Giày Adidas Stan Smith trắng xanh - thể thao',
        'quantity_in_stock': 25,
        'sell_price': 2200000
    },
    {
        'product_id': 'S003',
        'product_name': 'Converse Chuck Taylor',
        'product_image': 'products/s003_shoe.png',
        'company': 'Converse',
        'product_description': 'Giày vải Converse Chuck Taylor - cổ cao',
        'quantity_in_stock': 35,
        'sell_price': 1800000
    },
    {
        'product_id': 'S004',
        'product_name': 'New Balance 990v6',
        'product_image': 'products/s004_shoe.png',
        'company': 'New Balance',
        'product_description': 'Giày chạy New Balance 990v6 - êm chân cao cấp',
        'quantity_in_stock': 20,
        'sell_price': 3500000
    },
    {
        'product_id': 'S005',
        'product_name': 'Puma RS-X',
        'product_image': 'products/s005_shoe.png',
        'company': 'Puma',
        'product_description': 'Giày Puma RS-X đẹp mắt - năng động',
        'quantity_in_stock': 28,
        'sell_price': 2000000
    },
    {
        'product_id': 'S006',
        'product_name': 'Vans Old Skool',
        'product_image': 'products/s006_shoe.png',
        'company': 'Vans',
        'product_description': 'Giày Vans Old Skool đen trắng - phong cách Skateboard',
        'quantity_in_stock': 32,
        'sell_price': 1950000
    },
    {
        'product_id': 'S007',
        'product_name': 'Clarks Wallabee',
        'product_image': 'products/s007_shoe.png',
        'company': 'Clarks',
        'product_description': 'Giày Clarks Wallabee da lộn - thoải mái ưu tiên',
        'quantity_in_stock': 18,
        'sell_price': 3200000
    },
    {
        'product_id': 'S008',
        'product_name': 'Skechers GO Walk',
        'product_image': 'products/s008_shoe.png',
        'company': 'Skechers',
        'product_description': 'Giày Skechers GO Walk - giày tập đi',
        'quantity_in_stock': 40,
        'sell_price': 1600000
    },
]

# Thêm sản phẩm
for data in shoes_data:
    Product.objects.create(**data)
    print(f"✓ {data['product_name']}")

print("\n" + "="*60)
print("✓ ĐÃ THÊM 8 SẢN PHẨM GIÀY CÙNG ẢNH!")
print("="*60)

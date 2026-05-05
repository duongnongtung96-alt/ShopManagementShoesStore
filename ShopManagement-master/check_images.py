import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from products.models import Product

print("Kiểm tra dữ liệu ảnh trong database:\n")
print("="*70)

for product in Product.objects.all():
    print(f"\nSản phẩm: {product.product_name}")
    print(f"  Product ID: {product.product_id}")
    print(f"  Product Image (string): {product.product_image}")
    print(f"  Product Image (name): {product.product_image.name if product.product_image else 'None'}")
    if product.product_image:
        print(f"  Product Image (url): {product.product_image.url}")
        print(f"  File exists: {os.path.exists(product.product_image.path) if product.product_image else 'N/A'}")
    print("-"*70)

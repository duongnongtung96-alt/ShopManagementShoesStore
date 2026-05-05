import os
import django
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from products.models import Product

# Dữ liệu sản phẩm giày với màu sắc cho ảnh
shoes_colors = {
    'S001': {'name': 'Nike Air Force 1', 'bg': '#FFFFFF', 'text': '#000000', 'accent': '#000000'},
    'S002': {'name': 'Adidas Stan Smith', 'bg': '#E8F0FF', 'text': '#000000', 'accent': '#2D7FBF'},
    'S003': {'name': 'Converse Chuck Taylor', 'bg': '#000000', 'text': '#FFFFFF', 'accent': '#FF0000'},
    'S004': {'name': 'New Balance 990v6', 'bg': '#CCCCCC', 'text': '#000000', 'accent': '#880000'},
    'S005': {'name': 'Puma RS-X', 'bg': '#FFE600', 'text': '#000000', 'accent': '#000000'},
    'S006': {'name': 'Vans Old Skool', 'bg': '#000000', 'text': '#FFFFFF', 'accent': '#FFFFFF'},
    'S007': {'name': 'Clarks Wallabee', 'bg': '#8B7355', 'text': '#FFFFFF', 'accent': '#D2B48C'},
    'S008': {'name': 'Skechers GO Walk', 'bg': '#E8E8E8', 'text': '#000000', 'accent': '#0066CC'},
}

# Tạo thư mục nếu chưa tồn tại
media_dir = 'media/products/'
if not os.path.exists(media_dir):
    os.makedirs(media_dir)

print("Tạo ảnh giày cho từng sản phẩm...\n")

for product_id, shoe_info in shoes_colors.items():
    # Tạo ảnh
    img = Image.new('RGB', (400, 400), shoe_info['bg'])
    draw = ImageDraw.Draw(img)
    
    # Vẽ hình giày đơn giản (hình elipse)
    shoe_color = shoe_info['accent']
    draw.ellipse([50, 150, 350, 350], fill=shoe_color, outline=shoe_color)
    draw.ellipse([80, 180, 320, 320], fill=shoe_info['bg'], outline=shoe_color)
    draw.rectangle([100, 150, 300, 200], fill=shoe_color)
    
    # Thêm tên sản phẩm
    try:
        font = ImageFont.truetype('arial.ttf', 24)
    except:
        font = ImageFont.load_default()
    
    # Vẽ text
    text = shoe_info['name']
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (400 - text_width) // 2
    text_y = 20
    draw.text((text_x, text_y), text, fill=shoe_info['text'], font=font)
    
    # Lưu ảnh
    filename = f"{product_id.lower()}_shoe.png"
    filepath = os.path.join(media_dir, filename)
    img.save(filepath)
    print(f"✓ Ảnh cho {shoe_info['name']}: {filename}")

print("\n" + "="*60)
print("✓ ĐÃ TẠO XONG CÁC ẢNH GIÀY!")
print("="*60)

# Cập nhật sản phẩm với ảnh
print("\nCập nhật ảnh vào sản phẩm...\n")

for product_id, shoe_info in shoes_colors.items():
    filename = f"{product_id.lower()}_shoe.png"
    try:
        product = Product.objects.get(product_id=product_id)
        product.product_image = f'products/{filename}'
        product.save()
        print(f"✓ {shoe_info['name']}: {filename}")
    except Product.DoesNotExist:
        print(f"✗ Không tìm thấy sản phẩm: {product_id}")

print("\n" + "="*60)
print("✓ HOÀN THÀNH!")
print("="*60)
print("\nHãy truy cập: http://127.0.0.1:8000/")
print("để xem các sản phẩm với ảnh mới!")

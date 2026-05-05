import os
import django
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from products.models import Product

# Dữ liệu giày với thiết kế ảnh chi tiết hơn
shoes_designs = {
    'S001': {
        'name': 'Nike Air Force 1',
        'bg_color': '#f5f5f5',
        'shoe_color': '#ffffff',
        'stripe_color': '#000000',
        'accent_color': '#000000'
    },
    'S002': {
        'name': 'Adidas Stan Smith',
        'bg_color': '#e3f2fd',
        'shoe_color': '#ffffff',
        'stripe_color': '#1565c0',
        'accent_color': '#2d7fbf'
    },
    'S003': {
        'name': 'Converse Chuck Taylor',
        'bg_color': '#1a1a1a',
        'shoe_color': '#000000',
        'stripe_color': '#ffffff',
        'accent_color': '#ff0000'
    },
    'S004': {
        'name': 'New Balance 990v6',
        'bg_color': '#e0e0e0',
        'shoe_color': '#cccccc',
        'stripe_color': '#666666',
        'accent_color': '#880000'
    },
    'S005': {
        'name': 'Puma RS-X',
        'bg_color': '#ffe600',
        'shoe_color': '#ffeb3b',
        'stripe_color': '#000000',
        'accent_color': '#ff6f00'
    },
    'S006': {
        'name': 'Vans Old Skool',
        'bg_color': '#2a2a2a',
        'shoe_color': '#1a1a1a',
        'stripe_color': '#ffffff',
        'accent_color': '#ffffff'
    },
    'S007': {
        'name': 'Clarks Wallabee',
        'bg_color': '#d4a574',
        'shoe_color': '#8b7355',
        'stripe_color': '#6b5344',
        'accent_color': '#d2b48c'
    },
    'S008': {
        'name': 'Skechers GO Walk',
        'bg_color': '#f0f0f0',
        'shoe_color': '#e8e8e8',
        'stripe_color': '#0066cc',
        'accent_color': '#00d4ff'
    },
}

media_dir = 'media/products/'
os.makedirs(media_dir, exist_ok=True)

print("Tạo ảnh giày chất lượng cao...\n")

for product_id, design in shoes_designs.items():
    # Tạo ảnh 500x500
    img = Image.new('RGB', (500, 500), design['bg_color'])
    draw = ImageDraw.Draw(img)
    
    # Vẽ bóng giày
    draw.ellipse([80, 320, 420, 380], fill='#00000020')
    
    # Vẽ thân giày (hình phức tạp hơn)
    # Phần trên giày
    draw.ellipse([100, 150, 400, 280], fill=design['shoe_color'], outline=design['stripe_color'], width=2)
    
    # Phần lưỡi giày
    draw.polygon([(150, 280), (350, 280), (340, 340), (160, 340)], fill=design['shoe_color'])
    
    # Dây giày
    for y in range(200, 280, 20):
        draw.line([(220, y), (280, y)], fill=design['stripe_color'], width=2)
    
    # Đường viền accent
    draw.line([(150, 220), (350, 220)], fill=design['accent_color'], width=3)
    
    # Vẽ brand name
    try:
        font_title = ImageFont.truetype('arial.ttf', 32)
        font_info = ImageFont.truetype('arial.ttf', 14)
    except:
        font_title = ImageFont.load_default()
        font_info = ImageFont.load_default()
    
    # Tên sản phẩm
    text = design['name']
    bbox = draw.textbbox((0, 0), text, font=font_title)
    text_width = bbox[2] - bbox[0]
    text_x = (500 - text_width) // 2
    draw.text((text_x, 30), text, fill=design['accent_color'], font=font_title)
    
    # Thương hiệu
    brand_text = product_id
    bbox = draw.textbbox((0, 0), brand_text, font=font_info)
    text_width = bbox[2] - bbox[0]
    text_x = (500 - text_width) // 2
    draw.text((text_x, 410), brand_text, fill='#666666', font=font_info)
    
    # Lưu ảnh
    filename = f"{product_id.lower()}_shoe.png"
    filepath = os.path.join(media_dir, filename)
    img.save(filepath, 'PNG')
    print(f"✓ {design['name']}: {filename}")

print("\n" + "="*60)
print("✓ ĐÃ TẠO XONG CÁC ẢNH CHẤT LƯỢNG CAO!")
print("="*60)

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from django.contrib.auth.models import User

# Tạo superuser nếu chưa tồn tại
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gmail.com', 'admin123')
    print("Superuser 'admin' đã được tạo thành công!")
    print("Username: admin")
    print("Password: admin123")
else:
    print("Superuser 'admin' đã tồn tại!")

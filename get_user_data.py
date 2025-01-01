import os
import django

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # 替換為您的 settings 模組
django.setup()

from django.contrib.auth.models import User

def list_users():
    users = User.objects.all()  # 獲取所有用戶
    print("List of users in the database:\n")
    for user in users:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Date Joined: {user.date_joined}")
        print(f"Is Superuser: {user.is_superuser}")
        print("-" * 30)

if __name__ == "__main__":
    list_users()

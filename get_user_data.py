import os
import django

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # 替換為您的 settings 模組
django.setup()

from django.contrib.auth.models import User
from web_tool.models import Profile  # 替換為包含 Profile 模型的應用名稱

def list_users():
    users = User.objects.all()  # 獲取所有用戶
    print("List of users in the database:\n")
    for user in users:
        try:
            profile = Profile.objects.get(user=user)
            subscribed_stocks = profile.selected_stocks2  # 獲取訂閱的股票
        except Profile.DoesNotExist:
            subscribed_stocks = "No stocks subscribed"
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Date Joined: {user.date_joined}")
        print(f"Is Superuser: {user.is_superuser}")
        print(f"Subscribed Stocks: {subscribed_stocks}")
        profile = Profile.objects.get(user=user)

        # 獲取並解析訂閱的股票
        subscribed_stocks = profile.selected_stocks2 or ""  # 確保不為 None
        stocks_list = subscribed_stocks.split(',') if subscribed_stocks else []

        # 列出所有訂閱的股票
        print("Current subscribed stocks:")
        for stock in stocks_list:
            print(stock)

if __name__ == "__main__":
    list_users()

from django.shortcuts import render
from django.http import HttpResponse #匯入http模組
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

import io
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import urllib, base64
import random

# 註冊用戶
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        # 確認用戶名未被註冊
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            # 創建用戶
            User.objects.create_user(username=username, password=password, email=email)
            messages.success(request, 'User registered successfully.')
            return redirect('login_user')
    return render(request, 'register.html')

# 登入用戶
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # 驗證用戶
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('analyze_stock')  # 登入後跳轉到股票分析頁面
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')

# 登出用戶
def logout_user(request):
    logout(request)
    return redirect('login_user')

def analyze_stock(request):
    heatmap_data = None  # 預設為無數據
    if request.method == 'POST':
        # 從 POST 請求中獲取資料
        stock_code = request.POST.get('stock_code')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # 模擬策略計算
        strategies = ["Method 1", "Method 2", "Method 3", "Method 4", "Method 5"]
        days = ["Day 1", "Day 2"]
        heatmap_data = {
            strategy: {day: random.choice(['cheap', 'fair', 'expensive']) for day in days}
            for strategy in strategies
        }

    return render(request, 'ana_stock.html', {'heatmap_data': heatmap_data})


def hello_world(request):
    time = datetime.now()
    return render(request, 'hello_world.html', locals())


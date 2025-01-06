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
from eps import get_current_price2, select_stock, get_stream
import yfinance as yf
import talib
import numpy as np

def show_stock_data(request):
    return render(request, 'stock_chart.html')

def get_stock_data(request):
    stock_code = request.GET.get('stock_code', 'AAPL')  # 默認為 AAPL
    start_date = request.GET.get('start_date', '2024-01-01')
    end_date = request.GET.get('end_date', '2024-12-31')

    # 下載股票數據
    data = yf.download(stock_code, start=start_date, end=end_date)

    if data.empty:
        return JsonResponse({"error": "No data found for the given stock code and date range."}, status=400)

    # 計算技術指標
    data['RSI'] = talib.RSI(data['Close'], timeperiod=14)  # RSI
    data['K'], data['D'] = talib.STOCH(data['High'], data['Low'], data['Close'])  # KD
    data['MACD'], data['MACD_signal'], data['MACD_hist'] = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)  # MACD
    data['Upper'], data['Middle'], data['Lower'] = talib.BBANDS(data['Close'], timeperiod=20)  # 布林通道
    data['ADX'] = talib.ADX(data['High'], data['Low'], data['Close'], timeperiod=14)  # ADX
    data['Plus_DI'] = talib.PLUS_DI(data['High'], data['Low'], data['Close'], timeperiod=14)  # DMI+
    data['Minus_DI'] = talib.MINUS_DI(data['High'], data['Low'], data['Close'], timeperiod=14)  # DMI-

    # 計算 MACD_hist 的前一日值
    data['MACD_hist_prev'] = data['MACD_hist'].shift(1)

    # 計算進出場訊號
    def get_entry_signal(row):
        signals = []
        if row['RSI'] < 30:
            signals.append("RSI")
        if row['K'] < 20:
            signals.append("KD")
        if row['Close'] <= row['Lower']:
            signals.append("Bollinger")
        if row['ADX'] < 20:
            signals.append("ADX")
        if row['MACD_hist'] > 0 and row['MACD_hist_prev'] <= 0:
            signals.append("MACD")
        return ", ".join(signals) if signals else ""

    def get_exit_signal(row):
        signals = []
        if row['RSI'] > 70:
            signals.append("RSI")
        if row['K'] > 80:
            signals.append("KD")
        if row['Close'] >= row['Upper']:
            signals.append("Bollinger")
        if row['ADX'] > 30:
            signals.append("ADX")
        if row['MACD_hist'] < 0 and row['MACD_hist_prev'] >= 0:
            signals.append("MACD")
        return ", ".join(signals) if signals else ""

    data['EntrySignal'] = data.apply(get_entry_signal, axis=1)
    data['ExitSignal'] = data.apply(get_exit_signal, axis=1)

    # 整理成 JSON 格式
    result = []
    for index, row in data.iterrows():
        result.append({
            "date": index.strftime('%Y-%m-%d'),
            "open": row['Open'],
            "high": row['High'],
            "low": row['Low'],
            "close": row['Close'],
            "volume": row['Volume'],
            "entry_signal": row['EntrySignal'],
            "exit_signal": row['ExitSignal']
        })

    return JsonResponse(result, safe=False)

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


from django.shortcuts import render
from django.http import HttpResponse #匯入http模組
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
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
    days = None
    if request.method == 'POST':
        # 從 POST 請求中獲取資料
        stock_code = request.POST.get('stock_code')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        #stockID = "2330"
        stockID = stock_code
        divd = select_stock.dividend_yield_method(stockID)# 股利法
        print(divd)
        bpsEpsData = select_stock.get_bps_eps_data(stockID)
        stock = yf.Ticker(stockID+".TW")
        hl = select_stock.high_low_price_method(stock) # 高低法
        print(hl)
        pb = select_stock.p_b_ratio(bpsEpsData,stock)  #本淨比法
        print(pb)
        pe = select_stock.p_e_ratio(bpsEpsData,stock)
        print(pe)
        print("-----------------")

        #date_range_start = pd.to_datetime(target_date) - pd.Timedelta(days=7)
        #date_range_end = pd.to_datetime(target_date) + pd.Timedelta(days=7)
        data = yf.download(stockID+".TW", start=start_date, end=end_date)
        data['Date'] = data.index
        data['Date'] = pd.to_datetime(data['Date'])

        # 取得股價資訊
        close_price = data['Close']

        # 模擬策略計算
        #strategies = ["Method 1", "Method 2", "Method 3", "Method 4", "Method 5"]
        #days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
        #heatmap_data = {
        #    strategy: {day: random.choice(['cheap', 'fair', 'expensive']) for day in days}
        #    for strategy in strategies
        #}
        function_result=[divd,hl,pb,pe]
        #results_dict = {
        #'2024-12-02': {'method_1': 'expensive', 'method_2': 'expensive', 'method_3': 'expensive', 'method_4': 'expensive'},
        #'2024-12-03': {'method_1': 'fair_to_expensive', 'method_2': 'expensive', 'method_3': 'expensive', 'method_4': 'expensive'},
        #}
        strategy_names = ["股利法", "高低價法", "本淨比法", "本益比法"]
        results_dict={}
        for date, price in close_price.items():
            formatted_date = date.strftime('%Y-%m-%d')  # 格式化日期
            results_dict[formatted_date] = {}  # 每個日期對應一個子字典
            
            for i, func in enumerate(function_result, start=1):
                strategy_name = strategy_names[i-1]  # 根據索引動態獲取策略名稱
                cheap_price, fair_price, expensive_price = func[0], func[1], func[2]
                
                # 判斷價格範圍
                if price < cheap_price:
                    results_dict[formatted_date][strategy_name] = "cheap"
                elif cheap_price <= price < fair_price:
                    results_dict[formatted_date][strategy_name] = "cheap_to_fair"
                elif fair_price <= price < expensive_price:
                    results_dict[formatted_date][strategy_name] = "fair_to_expensive"
                else:
                    results_dict[formatted_date][strategy_name] = "expensive"

        days = list(results_dict.keys())  # 提取日期作為天數

        heatmap_data = {strategy: {day: results_dict[day][strategy] for day in days} for strategy in strategy_names}

    return render(request, 'ana_stock.html', {'days': days,'heatmap_data': heatmap_data})

from .models import Profile
from django.contrib.auth.decorators import login_required
import json

def save_stock(request):
    print("save_stock")
    if request.method == "POST":
        # 獲取當前用戶
        user = request.user
        # 獲取股票代號
        data = json.loads(request.body)
        stock_code = data.get("stock_code", "")

        # 更新模型
        profile, created = Profile.objects.get_or_create(user=user)
        
        # 獲取現有的股票代號，將新代號附加進去
        if profile.selected_stocks2:
            current_stocks = profile.selected_stocks2.split(',')  # 分解現有股票代號
        else:
            current_stocks = []
        
        # 防止重複添加
        if stock_code not in current_stocks:
            current_stocks.append(stock_code)
        
        # 保存更新的股票代號列表
        profile.selected_stocks2 = ','.join(current_stocks)
        profile.save()

        return JsonResponse({"message": "股票代號已保存！"}, status=200)

    return JsonResponse({"message": "無效請求"}, status=400)

@login_required
def delete_stock(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        stock_code = data.get("stock_code", "")

        profile, created = Profile.objects.get_or_create(user=user)
        if profile.selected_stocks2:
            stocks = profile.selected_stocks2.split(',')
            if stock_code in stocks:
                stocks.remove(stock_code)
                profile.selected_stocks2 = ','.join(stocks)  # 更新保存的股票
                profile.save()

        return JsonResponse({"message": "股票已刪除！"}, status=200)

    return JsonResponse({"message": "無效請求"}, status=400)

@login_required
def check_save(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    print("check_save")

    # 將保存的股票代號分解成列表（假設用逗號分隔多個代號）
    saved_stocks = profile.selected_stocks2.split(',') if profile.selected_stocks2 else []
    print(saved_stocks)

    return render(request, 'check_save.html', {'saved_stocks': saved_stocks})

def hello_world(request):
    time = datetime.now()
    return render(request, 'hello_world.html', locals())


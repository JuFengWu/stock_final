from django.shortcuts import render
from django.http import HttpResponse #匯入http模組
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import io
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import urllib, base64
import random


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


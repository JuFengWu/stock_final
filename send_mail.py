import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

def send_mail(receiver_email, body2, stock):

    sender_email = "jufengwu102000@gmail.com"

    password = ""

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = Header('Test Send Email', 'utf-8').encode()

    body = 'Hi! \n 你訂閱的股票'+stock+'狀態如下\n'
    body+= body2

    msg_content = MIMEText(body)
    msg.attach(msg_content)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        # 465是標準的SMTP-over-SSL端口
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("success send email")

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
            data = process(stock)
            result = ""
            for date, methods in data.items():
                formatted_string = f"{date}:\n{methods}\n"
                result += formatted_string
            send_mail("leowu102000@gmail.com",result,stock)

from eps import get_current_price2, select_stock, get_stream
import yfinance as yf
import pandas as pd
from datetime import datetime
def process(stock_code):
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
        today = datetime.today().strftime('%Y-%m-%d')
        lastDay = "2025-01-01"
        today = "2025-01-07"
        data = yf.download(stockID+".TW", start=lastDay, end=today)
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

        print(str(results_dict))
        return results_dict


if __name__ == "__main__":
    list_users()
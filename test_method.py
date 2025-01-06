from eps import get_current_price2, select_stock, get_stream
import yfinance as yf
import pandas as pd

stockID = "2330"

divd = select_stock.dividend_yield_method(stockID)# 股利法
print(divd)
bpsEpsData = select_stock.get_bps_eps_data(stockID)

target_date = "2024-12-01"

# 定義日期範圍 (查詢目標日期前後一週的數據)
date_range_start = pd.to_datetime(target_date) - pd.Timedelta(days=7)
date_range_end = pd.to_datetime(target_date) + pd.Timedelta(days=7)
data = yf.download(stockID+".TW", start=date_range_start, end=date_range_end)
data['Date'] = data.index
data['Date'] = pd.to_datetime(data['Date'])

# 找到距離目標日期最近的交易日
target_date = pd.to_datetime(target_date)
data['Date_Diff'] = abs(data['Date'] - target_date)
closest_row = data.loc[data['Date_Diff'].idxmin()]

# 取得股價資訊
closest_date = closest_row['Date']
open_price = closest_row['Open']
high_price = closest_row['High']
low_price = closest_row['Low']
close_price = closest_row['Close']
volume = closest_row['Volume']



stock = yf.Ticker(stockID+".TW")
"""
hl = select_stock.high_low_price_method(stock) # 高低法
print(hl)
pb = select_stock.p_b_ratio(bpsEpsData,stock)  #本淨比法
print(pb)
pe = select_stock.p_e_ratio(bpsEpsData,stock)
print(pe)
print("-----------------")

data =get_stream.get_stream(stockID)
print(data)
"""
print(close_price)
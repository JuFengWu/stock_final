from eps import get_current_price2, select_stock, get_stream
import yfinance as yf
import pandas as pd
stock_code = "2330"
start_date = "2024-12-01"
end_date = "2024-12-15"

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

function_result=[divd,hl,pb,pe]

# 儲存結果
results_dict = {}
data = yf.download(stockID+".TW", start=start_date, end=end_date)
data['Date'] = data.index
data['Date'] = pd.to_datetime(data['Date'])

# 取得股價資訊
value = data['Close']
print(value)
print("===")

for date, price in value.items():
    formatted_date = date.strftime('%Y-%m-%d')  # 格式化日期
    results_dict[formatted_date] = {}  # 每個日期對應一個子字典
    for i, func in enumerate(function_result, start=1):
        cheap_price, fair_price, expensive_price = func[0], func[1], func[2]
        
        # 判斷價格範圍
        if price < cheap_price:
            results_dict[formatted_date][f"method_{i}"] = "cheap"
        elif cheap_price <= price < fair_price:
            results_dict[formatted_date][f"method_{i}"] = "cheap_to_fair"
        elif fair_price <= price < expensive_price:
            results_dict[formatted_date][f"method_{i}"] = "fair_to_expensive"
        else:
            results_dict[formatted_date][f"method_{i}"] = "expensive"

# 列印結果字典
#for date, ranges in results_dict.items():
#    print(f"{date}: {ranges}")
print(results_dict)
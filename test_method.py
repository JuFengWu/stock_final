from eps import get_current_price2, select_stock, get_stream
import yfinance as yf

stockID = "2330"
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

data =get_stream.get_stream(stockID)
print(data)
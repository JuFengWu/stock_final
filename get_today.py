from datetime import datetime, timedelta
# 獲取今天的日期
today = datetime.today()

# 計算前七天的日期
seven_days_ago = today - timedelta(days=7)

# 將日期格式化為字串
seven_days_ago_str = seven_days_ago.strftime('%Y-%m-%d')
today_str = today.strftime('%Y-%m-%d')

print("今天:", today_str)
print("前七天:", seven_days_ago_str)
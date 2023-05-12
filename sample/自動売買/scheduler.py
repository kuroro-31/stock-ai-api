# 毎営業日の15:30にstock_processing.pyのmain()関数が実行
import schedule
import time
from datetime import datetime
import pytz
from stock_processing import main as stock_processing_main

def is_weekday():
    today = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%A')
    return today not in ['Saturday', 'Sunday']

def your_function():
    if is_weekday():
        stock_processing_main()

# スケジュールの設定
schedule.every().day.at("15:30").do(your_function)

while True:
    schedule.run_pending()
    time.sleep(60)

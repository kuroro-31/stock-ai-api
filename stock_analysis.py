# 株価データの取得と分析：
# a. Pythonで株価データを取得するためのライブラリ（pandas, yfinanceなど）をインストールします。
# b. 毎営業日の15:30に自動実行するスケジュールを設定します（scheduleライブラリが役立ちます）。
# c. 株価データを取得し、上昇率を計算します。
# SBI証券での自動売買：
# a. SBI証券APIを利用して株の売買を自動化します。APIの認証情報を取得して、Pythonプログラムに組み込みます。
# b. 上昇率が最も高い銘柄を選択し、現物1株を次の営業日の9:00に自動で購入します。
# 買った株価のモニタリングと売却条件：
# a. 購入価格の+50円になったら売却するように条件を設定します。
# b. 14:50になっても+50円に達しない場合は、その日のうちにプラスになる場合のみ売却します。
# c. 購入価格よりマイナスの場合、次の営業日にプラスになったタイミングで売却します。

import pandas_market_calendars as mcal
import yfinance as yf
import pandas_datareader.data as pdr
import datetime
import numpy as np

yf.pdr_override()

# 日本の営業日カレンダーを取得
jp_calendar = mcal.get_calendar('JPX')

# 今日より前の過去30日間の営業日を取得
today = datetime.date.today()
start_date = today - datetime.timedelta(days=30)
schedule = jp_calendar.schedule(start_date=start_date, end_date=today)
prev_day = schedule.iloc[-1].name.date()

# 日本株の銘柄コードリスト
stocks = [
    '3086.T', '3105.T', '3231.T', '3254.T', '3281.T', '3283.T', '3289.T', '3319.T', '3323.T', '3349.T',
    '3360.T', '3401.T', '3402.T', '3407.T', '3436.T', '3437.T', '3462.T', '3479.T', '3549.T', '3626.T',
    '3659.T', '3668.T', '3672.T', '3738.T', '3765.T', '3774.T', '3861.T', '3865.T', '3938.T', '3941.T',
    '4021.T', '4041.T', '4042.T', '4043.T', '4046.T', '4061.T', '4062.T', '4063.T', '4091.T', '4099.T',
    '4182.T', '4183.T', '4185.T', '4188.T', '4202.T', '4203.T', '4204.T', '4205.T', '4206.T', '4208.T',
    '4272.T', '4301.T', '4307.T', '4324.T', '4344.T', '4401.T', '4403.T', '4452.T', '4502.T', '4503.T',
    '4506.T', '4507.T', '4508.T', '4509.T', '4519.T', '4523.T', '4527.T', '4528.T', '4543.T', '4544.T',
    '4555.T', '4565.T', '4568.T', '4569.T', '4571.T', '4578.T', '4581.T', '4587.T', '4612.T', '4613.T',
    '4617.T', '4631.T', '4661.T', '4681.T', '4684.T', '4689.T', '4704.T', '4707.T', '4708.T', '4716.T',
    '4746.T', '4751.T', '4755.T', '4759.T', '4768.T', '4769.T', '4809.T', '4812.T', '4819.T', '4842.T',
    '4849.T', '4911.T', '4919.T', '4921.T', '4922.T', '4927.T', '4971.T', '4974.T', '4985.T', '5020.T',
    '5021.T', '5101.T', '5108.T', '5110.T', '5116.T', '5191.T', '5201.T', '5202.T', '5210.T', '5214.T',
    '5232.T', '5233.T', '5237.T', '5281.T', '5301.T', '5331.T', '5332.T', '5333.T', '5384.T', '5401.T',
    '5406.T', '5408.T', '5411.T', '5413.T', '5423.T', '5444.T', '5449.T', '5463.T', '5464.T', '5486.T',
    '5541.T', '5542.T', '5631.T', '5649.T', '5703.T', '5706.T', '5711.T', '5713.T', '5714.T', '5738.T', 
    '5801.T', '5802.T', '5803.T', '5805.T', '5901.T',
    '5951.T', '6005.T', '6028.T', '6103.T', '6104.T', '6113.T', '6118.T', '6135.T', '6136.T', '6141.T',
    '6175.T', '6178.T', '6184.T', '6191.T', '6195.T', '6196.T', '6198.T', '6201.T', '6269.T', '6273.T',
    '6279.T', '6292.T', '6301.T', '6302.T', '6305.T', '6308.T', '6324.T', '6326.T', '6327.T', '6360.T',
    '6361.T', '6366.T', '6367.T', '6368.T', '6369.T', '6370.T', '6395.T', '6412.T', '6417.T', '6425.T',
    '6436.T', '6445.T', '6448.T', '6457.T', '6460.T', '6471.T', '6472.T', '6473.T', '6479.T', '6481.T',
    '6501.T', '6502.T', '6503.T', '6504.T', '6505.T', '6506.T', '6508.T', '6572.T', '6586.T', '6592.T',
    '6594.T', '6599.T', '6617.T', '6632.T', '6641.T', '6645.T', '6656.T', '6674.T', '6701.T', '6702.T',
    '6703.T', '6723.T', '6724.T', '6728.T', '6740.T', '6750.T', '6752.T', '6753.T', '6754.T', '6758.T',
    '6762.T', '6764.T', '6770.T', '6777.T', '6841.T', '6857.T', '6869.T', '6902.T', '6905.T', '6952.T',
    '6954.T', '6971.T', '6976.T', '6981.T', '6995.T', '7004.T', '7011.T', '7012.T', '7013.T', '7181.T',
    '7182.T', '7186.T', '7201.T', '7202.T', '7203.T', '7211.T', '7261.T', '7267.T', '7269.T', '7270.T',
    '7272.T', '7276.T', '7278.T', '7313.T', '7731.T', '7733.T', '7735.T', '7762.T', '7832.T', '7911.T',
    '7912.T', '8028.T', '8053.T', '8058.T', '8233.T', '8252.T', '8253.T', '8260.T', '8267.T', '8303.T',
    '8304.T', '8305.T', '8306.T', '8308.T', '8309.T', '8316.T', '8324.T', '8586.T', '8591.T', '8593.T',
    '8601.T', '8604.T', '8609.T', '8628.T', '8630.T', '8697.T', '8725.T', '8750.T', '8766.T', '8795.T', 
    '8801.T', '8802.T', '8804.T', '8830.T',
    '8876.T', '9001.T', '9005.T', '9007.T', '9008.T', '9009.T', '9020.T', '9022.T', '9062.T', '9064.T',
    '9101.T', '9104.T', '9105.T', '9107.T', '9202.T', '9301.T', '9412.T', '9432.T', '9433.T', '9434.T',
    '9437.T', '9449.T', '9501.T', '9502.T', '9503.T', '9531.T', '9532.T', '9613.T', '9735.T', '9766.T',
    '9983.T', '9984.T', '9987.T'
]

# 営業日のデータを取得
data = {}
errors = []
for symbol in stocks:
    try:
        stock_data = yf.download(symbol, start=schedule.iloc[0].name.date(), end=today)
        if not stock_data.empty:
            data[symbol] = stock_data
    except Exception as e:
        errors.append((symbol, e))
        continue

if errors:
    for symbol, error in errors:
        print(f"Error fetching data for {symbol}: {error}")
# RSIを計算する関数
# RSIは、一定期間の上昇幅と下落幅を比較して、過買いや過売りの状態を示す指標です。
# RSIが70以上になると過買い状態を示し、30以下になると過売り状態を示すことが一般的です。
def compute_RSI(data, window=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

# MACDを計算する関数
# MACDは、異なる期間の移動平均線の差を計算し、それに基づいてトレンドの転換点を予測します。
# MACDのラインとシグナルのラインのクロスオーバーやヒストグラムの変化などを観察することで、上昇トレンドや下降トレンドの形成を確認することができます。
def compute_MACD(data, short_window=12, long_window=26, signal_window=9):
    exp1 = data.ewm(span=short_window, adjust=False).mean()
    exp2 = data.ewm(span=long_window, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

# ボリンジャーバンドを計算する関数
def compute_bollinger_bands(data, window=20):
    sma = data.rolling(window=window).mean()
    std = data.rolling(window=window).std()
    upper_band = sma + (2 * std)
    lower_band = sma - (2 * std)
    
    return sma, upper_band, lower_band

# 上昇が期待される銘柄と上昇率を抽出
rising_stocks = []
for symbol in stocks:
    if symbol in data and len(data[symbol]) >= 2:
        data[symbol]['SMA'] = data[symbol]['Adj Close'].rolling(window=5).mean()
        data[symbol]['EMA'] = data[symbol]['Adj Close'].ewm(span=5, adjust=False).mean()
        data[symbol]['RSI'] = compute_RSI(data[symbol]['Adj Close'])
        data[symbol]['MACD'], data[symbol]['Signal'] = compute_MACD(data[symbol]['Adj Close'])
        data[symbol]['BB_SMA'], data[symbol]['BB_Upper'], data[symbol]['BB_Lower'] = compute_bollinger_bands(data[symbol]['Adj Close'])
        
        if (data[symbol]['SMA'][-1] > data[symbol]['SMA'][-2] and
            data[symbol]['EMA'][-1] > data[symbol]['EMA'][-2] and
            data[symbol]['RSI'][-1] > 30 and
            data[symbol]['MACD'][-1] > data[symbol]['Signal'][-1] and
            data[symbol]['Adj Close'][-1] > data[symbol]['BB_SMA'][-1]):
            
            growth_rate = (data[symbol]['EMA'][-1] - data[symbol]['EMA'][-2]) / data[symbol]['EMA'][-2] * 100

            if symbol not in [stock[0] for stock in rising_stocks]:
                rising_stocks.append((symbol, growth_rate))

# 上昇率が高い順に銘柄をソート
rising_stocks = sorted(rising_stocks, key=lambda x: x[1], reverse=True)




import schedule
import time
from datetime import datetime
import pytz

def is_weekday():
    today = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%A')
    return today not in ['Saturday', 'Sunday']



def print_rising_stocks():
    rising_stocks = get_rising_stocks()
    if rising_stocks:
        print("上昇が期待される銘柄と上昇率:")
        for i, stock in enumerate(rising_stocks[:10]):
            print(f"{i+1}. {stock[0]}: {stock[1]:.2f}%")

if __name__ == '__main__':
    rising_stocks = get_rising_stocks()
    print("上昇が期待される銘柄と上昇率:")
    for i, stock in enumerate(rising_stocks[:10]):
        print(f"{i+1}. {stock[0]}: {stock[1]:.2f}%")

# スケジュールの設定
schedule.every().day.at("15:30").do(print_rising_stocks)

while True:
    schedule.run_pending()
    time.sleep(60)

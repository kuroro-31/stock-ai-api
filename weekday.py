#
# --------------------------------------------------------------------------
#  曜日の上昇率を計算します
# --------------------------------------------------------------------------
#
import yfinance as yf
import pandas as pd


def remove_outliers(df, column_name):
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]


# 銘柄を指定します。例: '7203.T' トヨタ自動車
ticker_symbol = '7203.T'

# yfinanceからデータを取得します
ticker_data = yf.Ticker(ticker_symbol)
historical_data = ticker_data.history(period='1d', start='2000-01-01')

# 前日の終値と比較して、株価が上がったかどうかを判断します
historical_data['Price_Up'] = historical_data['Close'].diff() > 0

# 異常値を除外します
historical_data = remove_outliers(historical_data, 'Close')

# 月ごとに分析します
for analyze_month in range(1, 13):
    print(f"Analysis for month: {analyze_month}")
    monthly_data = historical_data[historical_data.index.month == analyze_month]

    # 曜日ごとの上昇の割合を計算します
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    percentage_increase = {}

    for i, day in enumerate(days):
        day_data = monthly_data[monthly_data.index.dayofweek == i]
        percentage_increase[day] = (day_data['Price_Up'].sum(
        ) / day_data.shape[0]) * 100 if day_data.shape[0] > 0 else 0

    # 結果を表示します
    for day, percentage in percentage_increase.items():
        print(f"{day}: {percentage:.2f}%")
    print("\n" + "="*50 + "\n")

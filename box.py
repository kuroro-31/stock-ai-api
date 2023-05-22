import yfinance as yf
import datetime

# 株価データを取得


def get_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    return df

# ボックス理論に基づいて売買の判断を行う関数


def box_trading_strategy(df, box_range):
    # 初期化
    in_position = False
    buy_price = 0.0
    sell_price = 0.0
    trades = []

    # ボックスの上限と下限を計算
    box_top = df['High'].rolling(window=box_range).max()
    box_bottom = df['Low'].rolling(window=box_range).min()

    # 売買の判断を行う
    for i in range(len(df)):
        close_price = df['Close'].iloc[i]

        if close_price >= box_top[i]:
            if not in_position:
                in_position = True
                buy_price = close_price
                trades.append(('Buy', df.index[i], buy_price))
        elif close_price <= box_bottom[i]:
            if in_position:
                in_position = False
                sell_price = close_price
                trades.append(('Sell', df.index[i], sell_price))

    return trades


if __name__ == "__main__":
    # 株価データを取得
    ticker = '9432.T'  # 銘柄コード
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=5*365)

    df = get_stock_data(ticker, start_date, end_date)

    # データの存在を確認
    if df.empty:
        print(f"No data found for {ticker}")
    else:
        # ボックス理論に基づいて売買の判断を行う
        box_range = 20  # ボックスの期間
        trades = box_trading_strategy(df, box_range)

        # 売買の結果を表示
        for trade in trades:
            print(trade)

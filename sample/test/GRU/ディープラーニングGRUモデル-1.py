import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GRU
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import accuracy_score
import yfinance as yf
import matplotlib.pyplot as plt

import datetime
today = datetime.date.today()

# スクレイピングで日経平均株価の登録銘柄コードを取得する
import requests
from bs4 import BeautifulSoup

url = "https://indexes.nikkei.co.jp/nkave/index/component?idx=nk225"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

tickers = []

# 銘柄コードが含まれているdivタグをすべて探す
rows = soup.find_all("div", {"class": "row component-list"})

for row in rows:
    # 銘柄コードが含まれているdivタグを探す
    ticker_div = row.find("div", {"class": "col-xs-3 col-sm-1_5"})
    if ticker_div:
        # テキストを取得し、トリムして末尾に'.T'を追加
        ticker = ticker_div.text.strip() + ".T"
        tickers.append(ticker)

# 結果を表示
for ticker in tickers:
    print(ticker)

# 株価予測結果を保存する辞書
prediction_results = {}

# スケーラーのインスタンス化
scaler = MinMaxScaler(feature_range=(0, 1))

# 各銘柄について
for ticker in tickers:
    # 株価データの取得
    data = yf.download(ticker, start="2020-01-01", end=today)
    if len(data) == 0:
        continue
    # データの前処理
    data = data[['Close']]
    scaled_data = scaler.fit_transform(data)
    x, y = [], []
    for i in range(60,len(scaled_data)):
        x.append(scaled_data[i-60:i,0])
        y.append(scaled_data[i,0])
    x, y = np.array(x), np.array(y)

    # データの分割
    split = int(0.8 * len(x))
    x_train = x[:split]
    y_train = y[:split]
    x_test = x[split:]
    y_test = y[split:]
    
    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
    x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))
    
    # GRUモデルの設定
    model = Sequential()
    model.add(GRU(50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(GRU(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer=Adam())

    # モデルの訓練
    model.fit(x_train, y_train, epochs=50, batch_size=64, verbose=0)

    # テストデータに対する予測
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    
    # 予測結果を辞書に保存
    prediction_results[ticker] = predictions[-1][0] - data['Close'].iloc[-1]

# 予測結果を上昇額の高い順に並び替え
sorted_results = dict(sorted(prediction_results.items(), key=lambda item: item[1], reverse=True))

# 予測結果の表示
for ticker, increase in sorted_results.items():
    print(f'Ticker: {ticker}, Predicted Increase: {increase}')

# モデルの精度計算
y_test_inv = scaler.inverse_transform(y_test.reshape(-1, 1))
accuracy = accuracy_score(np.where(y_test_inv[1:] > y_test_inv[:-1], 1, 0), np.where(predictions[1:] > predictions[:-1], 1, 0))

print(f'Model Accuracy: {accuracy}')
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam, RMSprop
from sklearn.metrics import accuracy_score
import yfinance as yf
import matplotlib.pyplot as plt

import datetime
today = datetime.date.today()

tickers = [
    '8058.T',
    # '8001.T',
    # '8031.T',
    # '8053.T',
    # '8002.T',
    # '8015.T',
    # '2768.T',
    # '8020.T',
]


# 結果を表示
for ticker in tickers:
    print(ticker)

# 株価予測結果を保存する辞書
prediction_results = {}

# スケーラーのインスタンス化
scaler = MinMaxScaler(feature_range=(0, 1))

# 銘柄について
for ticker in tickers:
    # 株価データの取得
    data = yf.download(ticker, start="2015-01-01", end=today)
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
    
    # LSTMモデルの設定
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=(x_train.shape[1],1)))  # LSTM layer
    model.add(Dropout(0.2))  # Dropout layer
    model.add(LSTM(100))  # LSTM layer
    model.add(Dropout(0.2))  # Dropout layer
    model.add(Dense(1))  # Dense layer
    model.compile(loss='mean_squared_error', optimizer=RMSprop(learning_rate=0.001))  # Use RMSprop optimizer and learning_rate

    # モデルの訓練
    model.fit(x_train, y_train, epochs=100, batch_size=64, verbose=0)  # Increase epochs

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
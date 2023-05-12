# 必要なライブラリのインポート
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
import datetime

today = datetime.date.today()

# データの取得
data = yf.download('8058.T', start='2010-01-01', end=today)

# クロージング価格のみを使用
close_price = data.iloc[:, 3:4].values

# データの正規化
scaler = MinMaxScaler()
close_price_scaled = scaler.fit_transform(close_price)

# 過去60日分のデータを使用して次の日の株価を予測
X_train = []
y_train = []

for i in range(60, len(close_price)):
    X_train.append(close_price_scaled[i-60:i, 0])
    y_train.append(close_price_scaled[i, 0])
    
X_train, y_train = np.array(X_train), np.array(y_train)

# LSTMへの入力に適した形に変形
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# LSTMネットワークの作成
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=1))

# モデルのコンパイルと学習
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=50, batch_size=32)

# モデルの予測結果をテキストとして表示
for i in range(60, len(data)):
    print(f"Date: {data.index[i]} - Actual price {close_price[i][0]}, Predicted price {predicted_stock_price[i-60][0]}")

# 最新の60日間のデータを用いて次の日の株価を予測
last_60_days = close_price_scaled[-60:]
last_60_days = np.reshape(last_60_days, (1, 60, 1))
next_day_price = model.predict(last_60_days)
next_day_price = scaler.inverse_transform(next_day_price)

print(f"Predicted price for the next day: {next_day_price[0][0]}")

# モデルの精度（整合率）の計算
mse = np.mean((real_stock_price.flatten() - predicted_stock_price.flatten()) ** 2)
accuracy = 1 - mse / np.var(real_stock_price.flatten())

print(f'Model Accuracy: {accuracy * 100:.2f}%')
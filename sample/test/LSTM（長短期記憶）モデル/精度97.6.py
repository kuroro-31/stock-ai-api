# 必要なパッケージをインストール
# !pip install yfinance pandas numpy sklearn tensorflow matplotlib

# パッケージをインポート
import yfinance as yf
import pandas as pd
import numpy as np
import math
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

import datetime
today = datetime.date.today()

# データ取得
data = yf.download('8058.T', start='2000-01-01', end=today)

# データの前処理
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(data[['Open', 'High', 'Low', 'Close', 'Volume']].values)

# 訓練データとテストデータの作成
window_size = 60  # ウィンドウサイズを60に変更
train_data_len = int(len(scaled_data) * 0.8)
train_data = scaled_data[0:train_data_len, :]
x_train_list, y_train_list = [], []

for i in range(window_size, len(train_data)):
    x_train_list.append(train_data[i-window_size:i, :])
    y_train_list.append(train_data[i, 3])  # 3は'Close'のインデックス

# リストからnumpy配列へ変換
x_train, y_train = np.array(x_train_list), np.array(y_train_list)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], x_train.shape[2]))

# LSTM モデルの設定
model = Sequential()
model.add(LSTM(200, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))  # ユニット数を増やす
model.add(Dropout(0.2))  # Dropout層の追加
model.add(LSTM(200, return_sequences=False))  # ユニット数を増やす
model.add(Dropout(0.2))  # Dropout層の追加
model.add(Dense(100))  # ユニット数を増やす
model.add(Dense(1))

# モデルのコンパイル
optimizer = Adam(learning_rate=0.001)  # 学習率を小さく設定
model.compile(optimizer=optimizer, loss='mean_squared_error')

# EarlyStoppingの設定
es = EarlyStopping(monitor='val_loss', patience=5)

# モデルの訓練
model.fit(x_train, y_train, batch_size=128, epochs=200, validation_split=0.2, callbacks=[es])  # バッチサイズを増やし、エポック数を増やす、検証データを設定、EarlyStoppingを設定

# テストデータの作成
test_data = scaled_data[train_data_len - window_size:, :]
x_test_list, y_test = [], data['Close'][train_data_len:]

for i in range(window_size, len(test_data)):
    x_test_list.append(test_data[i-window_size:i, :])

# リストからnumpy配列へ変換
x_test = np.array(x_test_list)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], x_test.shape[2]))

# モデルの予測
predictions = model.predict(x_test)
close_scaler = MinMaxScaler().fit(data[['Close']].values)  # 'Close'に対するスケーラを作成
predictions = close_scaler.inverse_transform(predictions)  # 逆変換は'Close'のスケーラを使用

# Calculate the differences between actual and predicted prices
valid = data[train_data_len:]
valid['Predictions'] = predictions
valid['Difference'] = valid['Predictions'] - valid['Close']

# Sort the dataframe by the difference in descending order
sorted_valid = valid.sort_values(by='Difference', ascending=False)

# Display the sorted dataframe
# print(sorted_valid)

# Calculate the accuracy of the model
mae = mean_absolute_error(valid['Close'], valid['Predictions'])
accuracy = (1 - mae / valid['Close'].mean()) * 100
print(f"Accuracy: {accuracy:.2f}%")

# Calculate the MAPE
def mean_absolute_percentage_error(y_true, y_pred): 
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

mape = mean_absolute_percentage_error(valid['Close'], valid['Predictions'])
print(f"MAPE: {mape:.2f}%")

# Sort the dataframe by date in descending order
sorted_valid = valid.sort_index(ascending=False)

# Display the actual and predicted close prices for each day
for date, row in sorted_valid.iterrows():
    print(f"Date: {date}, Actual Close: {row['Close']}, Predicted Close: {row['Predictions']}")

# 翌日の株価を予測
new_df = data[['Open', 'High', 'Low', 'Close', 'Volume']].values[-window_size:]
scaled_new_df = scaler.transform(new_df)  # 全特徴量のスケーラを使用

x_test_new = np.array([scaled_new_df])
x_test_new = np.reshape(x_test_new, (1, x_test_new.shape[1], x_test_new.shape[2]))

predicted_price = model.predict(x_test_new)
predicted_price = close_scaler.inverse_transform(predicted_price)  # 逆変換は'Close'のスケーラを使用

# 翌日の日付を取得
next_day = today + datetime.timedelta(days=1)

# 小数点以下1桁を切り捨て
predicted_price = math.floor(predicted_price[0][0] * 10) / 10

print(f"次の日（{next_day}）の予想クローズ価格: {predicted_price}円")
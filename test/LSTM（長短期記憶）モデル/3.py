# 必要なパッケージをインストール
# !pip install yfinance pandas numpy sklearn tensorflow matplotlib

# パッケージをインポート
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

import datetime
today = datetime.date.today()

# データ取得
data = yf.download('8058.T', start='2013-01-01', end=today)

# データの前処理
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))

# 訓練データとテストデータの作成
train_data_len = int(len(scaled_data) * 0.8)
train_data = scaled_data[0:train_data_len, :]
x_train, y_train = [], []

for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# LSTM モデルの設定
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

# モデルのコンパイル
model.compile(optimizer='adam', loss='mean_squared_error')

# モデルの訓練
model.fit(x_train, y_train, batch_size=1, epochs=1)

# テストデータの作成
test_data = scaled_data[train_data_len - 60:, :]
x_test, y_test = [], data['Close'][train_data_len:]

for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# モデルの予測
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# Calculate the differences between actual and predicted prices
valid = data[train_data_len:]
valid['Predictions'] = predictions
valid['Difference'] = valid['Predictions'] - valid['Close']

# Calculate the accuracy of the model
mae = mean_absolute_error(valid['Close'], valid['Predictions'])
accuracy = (1 - mae / valid['Close'].mean()) * 100
print(f"Accuracy: {accuracy:.2f}%")

# Sort the dataframe by the difference in descending order
sorted_valid = valid.sort_values(by='Difference', ascending=False)

# Display the sorted dataframe
# print(sorted_valid)

# Sort the dataframe by date in descending order
sorted_valid = valid.sort_index(ascending=False)

# Display the actual and predicted close prices for each day
for date, row in sorted_valid.iterrows():
    print(f"Date: {date}, Actual Close: {row['Close']}, Predicted Close: {row['Predictions']}")

# 翌日の株価を予測
new_df = data['Close'].values[-60:].reshape(-1,1)
scaled_new_df = scaler.transform(new_df)

x_test_new = np.array(scaled_new_df)
x_test_new = np.reshape(x_test_new, (1, x_test_new.shape[0], 1))

predicted_price = model.predict(x_test_new)
predicted_price = scaler.inverse_transform(predicted_price)

# 翌日の日付を取得
next_day = today + datetime.timedelta(days=1)

print(f"次の日（{next_day}）の予想クローズ価格: {predicted_price[0,0]}")
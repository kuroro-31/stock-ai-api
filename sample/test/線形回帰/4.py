import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import math

# Step 1: スクレイピングで東証一部上場企業銘柄コードを取得
url = "https://ja.wikipedia.org/wiki/%E6%9D%B1%E4%BA%AC%E8%A8%BC%E5%88%B8%E5%8F%96%E5%BC%95%E6%89%80%E3%83%97%E3%83%A9%E3%82%A4%E3%83%A0%E5%B8%82%E5%A0%B4%E4%B8%8A%E5%A0%B4%E4%BC%81%E6%A5%AD%E4%B8%80%E8%A6%A7"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
tickers = []
table = soup.find("table", {"class": "sortable wikitable"})
for row in table.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) > 0:
        ticker = cells[0].text.strip() + ".T"
        tickers.append(ticker)

# Step 2: 各銘柄の株価データを取得
data_frames = []
for ticker in tickers:
    data = yf.download(ticker, period="1y")
    if not data.empty:
        data['Ticker'] = ticker
        data_frames.append(data)
all_data = pd.concat(data_frames)

# Step 3: 線形回帰モデルを学習
all_data['Return'] = all_data['Close'].pct_change()
all_data.dropna(inplace=True)

X = all_data['Close'].values.reshape(-1,1)
y = all_data['Return'].values.reshape(-1,1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Step 4: 予測と評価
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f"Model R^2 Score: {math.floor(r2 * 10000) / 100}%")  # R^2スコアをパーセンテージに変換し、小数点2位以下を切り捨てる

# 銘柄毎の翌日の株価上昇率を予測
forecast = []
for ticker in tickers:
    latest_price = all_data[all_data['Ticker'] == ticker]['Close'].iloc[-1]
    predicted_return = model.predict([[latest_price]])
    forecast.append((ticker, predicted_return[0][0]))

# 上昇率が高い順に銘柄を並び替え
forecast = sorted(forecast, key=lambda x: x[1], reverse=True)

# 結果の表示
for ticker, predicted_return in forecast[:10]:
    predicted_return_percent = math.floor(predicted_return * 10000) / 100  # 上昇率をパーセンテージに変換し、小数点2位以下を切り捨てる
    print(f"Ticker: {ticker}, Predicted Return: {predicted_return_percent}%")
# 過去15年間のデータを用いて機械学習モデルを訓練し、翌日の株価の上昇期待額が最も高い銘柄を取得します。
# また、モデルの整合率（R²スコア）も表示されます。上記のコードを Google Colab に貼り付けて実行すると、期待される結果が得られます。

# !pip install yfinance pandas numpy scikit-learn
# !pip install requests
# !pip install beautifulsoup4

import yfinance as yf
import pandas as pd
import numpy as np
import datetime
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import requests
from bs4 import BeautifulSoup

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

today = datetime.date.today()
start_date = today - datetime.timedelta(days=15*365)

predictions = []

for ticker in tickers:
    try:
        data = yf.download(ticker, start=start_date, end=today)
        
        if data.empty:
            continue

        data['prediction'] = data['Close'].shift(-1)
        X = np.array(data.drop(['prediction'], axis=1))
        X = X[:-1]
        y = np.array(data['prediction'])
        y = y[:-1]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)

        x_future = np.array(data.drop(['prediction'], axis=1))[-1:]
        predicted_price = model.predict(x_future)
        
        change_percentage = (predicted_price[0] - data['Close'][-1]) / data['Close'][-1] * 100
        predictions.append((ticker, change_percentage, r2))
    except Exception as e:
        print(f"Error processing ticker '{ticker}': {e}")

predictions.sort(key=lambda x: x[1], reverse=True)

for symbol, percentage, r2 in predictions:
    print(f"{symbol}: {percentage:.2f}% (R²: {r2:.2f})")
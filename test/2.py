# 上昇率
# このコードは、線形回帰モデルを使用して、日本の株式市場における各銘柄の翌日の株価を予測しています。具体的な手順は以下の通りです。

# 銘柄コードリスト（tickers）から、各銘柄の株価データを取得します。
# 取得した株価データに基づいて、特徴量（X）とターゲット変数（y）を準備します。ここでは、特徴量は株価データそのものであり、ターゲット変数は翌日の終値です。
# データを学習用（80%）とテスト用（20%）に分割します。
# 線形回帰モデル（LinearRegression）を使用して、学習用データをもとにモデルを学習させます。
# 学習したモデルを使用して、最新の株価データ（x_future）に基づいて翌日の株価（predicted_price）を予測します。
# 予測された翌日の株価と現在の終値を比較し、変化率（change_percentage）を計算します。
# 最後に、銘柄と予測結果（変化率）をpredictionsリストに追加します。
# このプロセスは、リスト内のすべての銘柄に対して繰り返されます。最終的なpredictionsリストには、各銘柄の翌日の株価の予測変化率が格納されます
# ただし、線形回帰は単純なモデルであるため、実際の株価予測には限定的な有用性しかありません。より高度な予測手法や追加の特徴量を使用することで、予測精度を向上させることができます。

# !pip install yfinance pandas numpy scikit-learn

import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

today = datetime.date.today()


# 日経平均株価の銘柄コードリスト
# WikipediaからPythonのBeautifulSoupというライブラリを用いたスクレイピングです。
# BeautifulSoupを使うことで、HTMLコードから特定の情報を抽出することができます。
# 銘柄コードをスクレイピングしました。
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

print(tickers)


predictions = []

for ticker in tickers:
    try:
        # 株価データを取得
        data = yf.download(ticker, start='2010-01-01', end=today)
        
        if data.empty:
            continue

        # 特徴量とターゲット変数を準備
        data['prediction'] = data['Close'].shift(-1)
        X = np.array(data.drop(['prediction'], axis=1))
        X = X[:-1]
        y = np.array(data['prediction'])
        y = y[:-1]
        
        # データを学習用とテスト用に分割
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # 線形回帰モデルを学習
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # モデルのR²スコアを計算
        y_pred = model.predict(X_test)
        r2_score = model.score(X_test, y_test)
        
        # 翌日の株価を予測
        x_future = np.array(data.drop(['prediction'], axis=1))[-1:]
        predicted_price = model.predict(x_future)
        
        # 銘柄と予測結果、R²スコアを保存
        change_percentage = (predicted_price[0] - data['Close'][-1]) / data['Close'][-1] * 100
        predictions.append((ticker, change_percentage, r2_score))
    except Exception as e:
        print(f"Error processing ticker '{ticker}': {e}")

# 上昇率が高い順にソートして出力
predictions.sort(key=lambda x: x[1], reverse=True)

for symbol, percentage, r2_score in predictions:
    print(f"{symbol}: {percentage:.2f}% (R²: {r2_score:.2f})")
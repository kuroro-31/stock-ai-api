# 経済状況: 経済指標（GDP、失業率、インフレ率など）を特徴量として使用することができます。ただし、これらの指標は定期的にしか更新されないため、その間の変動を捉えることが難しい場合があります。

# 業績: 企業の財務データ（売上高、営業利益、純利益など）や株価指標（PER、PBR、配当利回りなど）を特徴量として使用することができます。これらのデータは定期的に更新されるため、モデルが業績の変化を考慮することができます。

# 市場ニュースやイベント: ニュース記事やプレスリリースをテキスト分析して、その内容を特徴量として使用することができます。自然言語処理（NLP）技術を活用して、ニュースやイベントの情報を数値化し、モデルに組み込むことができます。

# セクター別の動向: 各企業が属するセクターや業界の動向を特徴量として使用することができます。たとえば、セクター別の株価指数や各業界の平均的な財務データなどを用いることができます。

# これらの要素をモデルに組み込むことで、予測精度を向上させることが期待できます。ただし、特徴量の選択やデータの前処理が適切であることが重要です。また、経済状況や市場ニュースなど、時系列データに特有のトレンドや季節性を考慮することも、予測精度を向上させるために重要です。これらの要素を組み込む際には、ディープラーニングや機械学習アルゴリズムの適用が有効です。

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
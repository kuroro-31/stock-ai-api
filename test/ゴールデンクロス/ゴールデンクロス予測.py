# 必要なライブラリをインポートします。
# 東京証券取引所プライム市場に上場している企業の銘柄コードをウェブスクレイピングを用いて取得します。
# 各銘柄について、過去の株価データを取得し、特徴量と目標変数を生成します。特徴量は各銘柄の5日間と25日間の移動平均とゴールデンクロスの有無、目標変数は株価の変化率です。
# データを訓練データとテストデータに分割し、ランダムフォレスト回帰モデルを訓練します。そして、訓練したモデルの平均二乗誤差を計算します。
# 各銘柄の最新の株価データを取得し、特徴量を生成します。
# ゴールデンクロスが発生した銘柄について、訓練したモデルを用いて株価の上昇率を予測します。
# 予測した上昇率が高い順に銘柄をソートし、表示しますimport pandas as pd
import numpy as np
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
import requests
from bs4 import BeautifulSoup

import datetime
today = datetime.date.today()

# スクレイピングで東証一部上場企業銘柄コードを取得する
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

# Define a function to create features and target
def create_features_target(data):
    data['Return'] = data['Close'].pct_change()
    data['MA5'] = data['Close'].rolling(5).mean()
    data['MA25'] = data['Close'].rolling(25).mean()
    data['GoldenCross'] = np.where(data['MA5'] > data['MA25'], 1, 0)
    data = data.dropna()
    
    features = data.drop(['Close', 'Return'], axis=1)
    target = data['Return']
    
    return features, target

# Initialize a list to store the models for each ticker
models = []

for ticker in tickers:
    data = yf.download(ticker, start='2018-01-01', end=today)
    
    # Check if the data is not empty
    if data.empty:
        print(f"No data for {ticker}, skipping...")
        continue

    # Create features and target
    X, y = create_features_target(data)

    # Check if the features and target are not empty
    if X.empty or y.empty:
        print(f"No valid data for {ticker}, skipping...")
        continue
    
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create a pipeline
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('pca', PCA()),
        ('model', RandomForestRegressor(random_state=42))
    ])

    # Fit the pipeline
    pipe.fit(X_train, y_train)

    # Predict the test set
    y_pred = pipe.predict(X_test)

    # Calculate the mean squared error of the model
    mse = mean_squared_error(y_test, y_pred)

    print(f'MSE for {ticker}: {mse}')

    # Store the model
    models.append((ticker, pipe))

# 最新の日付を取得
latest_date = datetime.datetime.now()

# ゴールデンクロスの銘柄と予測上昇額を保存するデータフレームを作成
golden_cross_df = pd.DataFrame(columns=['ticker', 'predicted_increase'])

for ticker, model in models:
    # 最新のデータをダウンロード
    data = yf.download(ticker, start='2018-01-01', end=latest_date.strftime('%Y-%m-%d'))
    
    # 特徴量を作成
    X_latest = create_features(data)
    
    # 予測を行う
    predicted_increase = model.predict(X_latest)
    
    # 平均を取ることで単一の予測値を得る
    predicted_increase = predicted_increase.mean()
    
    # ゴールデンクロスを判定
    if is_golden_cross(data):
        # ゴールデンクロスの場合、予測上昇額をデータフレームに追加
        new_row = pd.DataFrame({'ticker': [ticker], 'predicted_increase': [predicted_increase]})
        golden_cross_df = pd.concat([golden_cross_df, new_row], ignore_index=True)

# 予測上昇額が大きい順にソート
golden_cross_df = golden_cross_df.sort_values(by='predicted_increase', ascending=False)

# 結果を表示
print(golden_cross_df)
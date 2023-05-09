# !pip install yfinance pandas bs4 requests

import requests
import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

# スクレイピングで東証一部上場企業銘柄コードを取得する
url = "https://ja.wikipedia.org/wiki/%E6%9D%B1%E4%BA%AC%E8%A8%BC%E5%88%B8%E5%8F%96%E5%BC%95%E6%89%80%E3%82%B0%E3%83%AD%E3%83%BC%E3%82%B9%E5%B8%82%E5%A0%B4%E4%B8%8A%E5%A0%B4%E4%BC%81%E6%A5%AD%E4%B8%80%E8%A6%A7"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

tickers = []


table = soup.find("table", {"class": "sortable wikitable"})
for row in table.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) > 0:
        ticker = cells[0].text.strip() + ".T"
        tickers.append(ticker)

# 結果を表示
for ticker in tickers:
    print(ticker)

for ticker in tickers:
    # Get historical market data
    hist = yf.Ticker(ticker).history(period="1y")
    
    if hist.empty:
        print(f"No data for ticker {ticker}")
        continue

    # Calculate SMA for 30 days
    hist['SMA'] = hist['Close'].rolling(window=150).mean()
    
    # Calculate prediction as difference between last close price and last SMA
    prediction = hist['Close'].iloc[-1] - hist['SMA'].iloc[-1]
    
    predictions[ticker] = prediction

# Create DataFrame from predictions
predictions_df = pd.DataFrame(list(predictions.items()), columns=['Ticker', 'Prediction'])

# Sort by prediction in descending order
predictions_df = predictions_df.sort_values('Prediction', ascending=False)

# Print the list of tickers expected to rise
print(predictions_df)
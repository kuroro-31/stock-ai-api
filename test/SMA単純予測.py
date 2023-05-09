# !pip install yfinance pandas bs4 requests

import requests
import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup

url = "https://indexes.nikkei.co.jp/nkave/index/component?idx=nk225"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

tickers = []

rows = soup.find_all("div", {"class": "row component-list"})
for row in rows:
    ticker_div = row.find("div", {"class": "col-xs-3 col-sm-1_5"})
    if ticker_div:
        ticker = ticker_div.text.strip() + ".T"
        tickers.append(ticker)

predictions = {}

for ticker in tickers:
    # Get historical market data
    hist = yf.Ticker(ticker).history(period="1y")
    
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
# スクレイピングで日経平均株価の登録銘柄コードを取得する
import requests
from bs4 import BeautifulSoup

url = "https://indexes.nikkei.co.jp/nkave/index/component?idx=nk225"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

tickers = []

# 銘柄コードが含まれているdivタグをすべて探す
rows = soup.find_all("div", {"class": "row component-list"})

for row in rows:
    # 銘柄コードが含まれているdivタグを探す
    ticker_div = row.find("div", {"class": "col-xs-3 col-sm-1_5"})
    if ticker_div:
        # テキストを取得し、トリムして末尾に'.T'を追加
        ticker = ticker_div.text.strip() + ".T"
        tickers.append(ticker)

# 結果を表示
for ticker in tickers:
    print(ticker)

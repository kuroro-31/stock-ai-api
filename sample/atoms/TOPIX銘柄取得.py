import requests
from bs4 import BeautifulSoup

url = "https://www.okasan-online.co.jp/jp/brand_topix100.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

tickers = []

# HTML構造に基づいて適切なセレクタを指定
rows = soup.find_all("tr")
for row in rows:
    # 銘柄コードが含まれているtd要素を探す
    ticker_tds = row.find_all("td", align="center")
    for td in ticker_tds:
        ticker = td.text.strip() + ".T"  # 日本の銘柄コードには".T"を追加
        tickers.append(ticker)

print(tickers)

import yfinance as yf
import datetime
import requests
import os

from tqdm import tqdm
from components.supatrade.login import login_supatrade, new_post, new_post_send

from components.webdriver_setup import setup_driver
from components.sbi.bank.login import login_sbi_bank
from components.ticker_prime import tickers  # 銘柄のリストをインポート

from components.notifications import send_message_to_slack

from components.config import APP_ENV
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from components.sbi.buy import main as buy_stock


# 購入数
purchase_number = 1


# 株価を取得
def get_stock_data(ticker):
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=60)
    df = yf.download(ticker, start, end)
    if df.empty:  # Check if the dataframe is empty
        print(f"No data for {ticker} from {start} to {end}")
        return df, None, None
    latest_price = df.iloc[-1]['Close']  # 終値を取得
    return df, end.strftime('%Y年%m月%d日'), latest_price


# 移動平均線を計算
def calculate_moving_averages(df):
    if len(df) < 25:  # データが25未満の場合はNoneを返す
        return None, None
    ma5 = df['Close'].rolling(window=5).mean()
    ma25 = df['Close'].rolling(window=25).mean()
    return ma5, ma25


# ポートフォリオに銘柄が含まれているかチェック
def check_portfolio(ticker):
    driver = setup_driver()

    try:
        login_sbi_bank(driver)

        # 残高照会ページに遷移
        driver.implicitly_wait(10)
        balance_check = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'm-icon-ps_balance'))
        )
        balance_check.click()

        # 詳細をクリック
        driver.implicitly_wait(50)
        details_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="SBI証券保有資産評価"]'))
        )
        details_button.click()

        # 詳細を選択
        driver.implicitly_wait(50)
        details_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "詳細")]'))
        )
        details_button.click()

        # ポートフォリオ情報を取得
        driver.implicitly_wait(50)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//p[contains(text(), "■株式（現物／特定預り）")]'))
        )

        # pタグのすぐ後にあるテーブルを取得する
        driver.implicitly_wait(50)
        table = driver.find_element(
            By.XPATH, '//p[contains(text(), "■株式（現物／特定預り）")]/following-sibling::div/table')

        # テーブルの銘柄すべてを取得する
        driver.implicitly_wait(50)
        rows = table.find_elements(By.XPATH, './/tbody/tr')

        # ポートフォリオに銘柄があるかどうかを確認し、Slackに通知する
        for row in rows:
            stock_code_text = row.find_element(By.XPATH, './/th').text
            stock_code_lines = stock_code_text.split('\n')  # 改行で分割
            if not stock_code_lines:
                continue
            stock_code = stock_code_lines[0]  # 最初の行を銘柄コードとして取り出す
            stock_code_with_suffix = stock_code + '.T'  # 銘柄コードに'.T'を追加
            print(stock_code_with_suffix)

            if ticker == stock_code_with_suffix:  # ここで比較
                return True  # ポートフォリオに銘柄がある場合、Trueを返す

        return False  # ループが終わってもreturnされなかった場合、銘柄はポートフォリオに存在しないので、Falseを返す

    except Exception as e:
        print(
            f'An error occurred while checking portfolio for {ticker}: {str(e)}')
        return False

    finally:
        driver.quit()


# クロスオーバーの確認
def check_crossover(ma5, ma25):
    if len(ma5) < 2 or len(ma25) < 2:  # データが2つ未満の場合は'hold'を返す
        return 'hold'
    if ma5.iloc[-2] < ma25.iloc[-2] and ma5.iloc[-1] > ma25.iloc[-1]:
        return 'buy'
    elif ma5.iloc[-2] > ma25.iloc[-2] and ma5.iloc[-1] < ma25.iloc[-1]:
        return 'sell'
    else:
        return 'hold'


if __name__ == "__main__":
    driver = setup_driver()
    buy_list = []
    sell_list = []
    title = ""
    buy_message = ""
    sell_message = ""

    for ticker in tqdm(tickers):
        df, date, latest_price = get_stock_data(ticker)
        if df.empty:
            print(f"No data for {ticker}")
            continue

        ma5, ma25 = calculate_moving_averages(df)
        if ma5 is None or ma25 is None:  # ma5またはma25がNoneの場合はスキップ
            print(f"Not enough data for {ticker}")
            continue

        if ma5.iloc[-2] < ma25.iloc[-2] and ma5.iloc[-1] > ma25.iloc[-1]:
            buy_list.append(f'【{ticker}】 終値: {latest_price}円')
        elif ma5.iloc[-2] > ma25.iloc[-2] and ma5.iloc[-1] < ma25.iloc[-1]:
            sell_list.append(f'【{ticker}】 終値: {latest_price}円')

    if buy_list:
        buy_message = '「買い」\n' + '\n'.join(buy_list)
        send_message_to_slack(buy_message)
    if sell_list:
        sell_message = '「売り」\n' + '\n'.join(sell_list)
        send_message_to_slack(sell_message, 'danger')

    title = '【短期】東証プライム シグナル'
    login_supatrade(driver)
    new_post(driver)
    new_post_send(driver, title, buy_message, sell_message)

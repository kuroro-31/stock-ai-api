import yfinance as yf
import datetime
import requests
import os

from components.webdriver_setup import setup_driver
from components.sbi.bank.login import login_sbi_bank
from components.tickers import tickers  # 銘柄のリストをインポート

from components.notifications import send_message_to_slack

from components.config import APP_ENV
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from components.sbi.buy import main as buy_stock

os.environ['SLACK_WEBHOOK_URL'] = 'https://hooks.slack.com/services/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'

# 購入数
purchase_number = 1


# 株価を取得
def get_stock_data(ticker):
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=60)
    df = yf.download(ticker, start, end)
    latest_price = df.iloc[-1]['Close']  # 最新の終値を取得
    return df, end.strftime('%Y年%m月%d日'), latest_price  # latest_priceを返り値に追加


# 移動平均線を計算
def calculate_moving_averages(df):
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
    if ma5[-2] < ma25[-2] and ma5[-1] > ma25[-1]:
        return 'buy'
    elif ma5[-2] > ma25[-2] and ma5[-1] < ma25[-1]:
        return 'sell'
    else:
        return 'hold'


if __name__ == "__main__":
    # 各銘柄について株価の取得、移動平均の計算、ポートフォリオのチェックを一度に行う
    for ticker in tickers:
        df, latest_date, latest_price = get_stock_data(ticker)
        ma5, ma25 = calculate_moving_averages(df)
        # in_portfolio = check_portfolio(ticker)

        # print(f'{ticker}')
        # print(f'5-day MA: {ma5.iloc[-1]}, 25-day MA: {ma25.iloc[-1]}')
        # print(f'Is in portfolio: {in_portfolio}')

        if ma5.iloc[-2] < ma25.iloc[-2] and ma5.iloc[-1] > ma25.iloc[-1]:
            send_message_to_slack(
                f'{latest_date}\n【{ticker}】\n「買い」の判定です。\n最新の終値: {latest_price}円')            # if not in_portfolio:  # ポートフォリオに銘柄がない場合
            #     send_message_to_slack(
            #         f'{latest_date}\n【{ticker}】\n「買い」の判定です。\n銘柄を買います。')

            #     # 'ticker'から'.T'を削除
            #     ticker_without_t = ticker.replace('.T', '')

            #     # 銘柄を購入する処理を追加します
            #     buy_stock(ticker_without_t, purchase_number)

            # else:  # ポートフォリオに銘柄がある場合
            #     send_message_to_slack(
            #         f'{latest_date}\n【{ticker}】\n「買い」の判定です。\n銘柄はすでに保持しています。')
            # elif ma5.iloc[-2] > ma25.iloc[-2] and ma5.iloc[-1] < ma25.iloc[-1]:
            #     if in_portfolio:  # ポートフォリオに銘柄がある場合
            #         send_message_to_slack(
            #             f'{latest_date}\n【{ticker}】\n「売り」の判定です。\n銘柄を売ります。', 'danger')
        elif ma5.iloc[-2] > ma25.iloc[-2] and ma5.iloc[-1] < ma25.iloc[-1]:
            send_message_to_slack(
                f'{latest_date}\n【{ticker}】\n「売り」の判定です。\n最新の終値: {latest_price}円', 'danger')        # else:
        #     print(f'{ticker} は「ホールド」の判定です。')
            # send_message_to_slack(
            #     f'{latest_date}\n【{ticker}】\n「保持」の判定です。')  # 買いでも売りでもない場合にもメッセージを送信します。

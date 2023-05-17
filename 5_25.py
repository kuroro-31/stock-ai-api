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


os.environ['SLACK_WEBHOOK_URL'] = 'https://hooks.slack.com/services/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'


def get_stock_data(ticker):
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=60)
    df = yf.download(ticker, start, end)
    return df, end.strftime('%Y年%m月%d日')


def calculate_moving_averages(df):
    ma5 = df['Close'].rolling(window=5).mean()
    ma25 = df['Close'].rolling(window=25).mean()
    return ma5, ma25


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
        table = driver.find_element(
            By.XPATH, '//p[contains(text(), "■株式（現物／特定預り）")]/following-sibling::div/table')

        # テーブルの銘柄すべてを取得する
        rows = table.find_elements(By.XPATH, './/tbody/tr')

        # ポートフォリオに銘柄があるかどうかを確認し、Slackに通知する
        for row in rows:
            stock_code = row.find_element(By.XPATH, './/th').text.split(' ')[0]
            if ticker in stock_code:
                send_message_to_slack(f'【{ticker}】はポートフォリオにあります。')
                return
        send_message_to_slack(f'【{ticker}】はポートフォリオにありません。', 'danger')

    finally:
        driver.quit()


def check_stock(ticker):
    df, latest_date = get_stock_data(ticker)
    ma5, ma25 = calculate_moving_averages(df)

    print(f'5-day MA: {ma5.iloc[-1]}, 25-day MA: {ma25.iloc[-1]}')

    if ma5.iloc[-1] > ma25.iloc[-1]:
        send_message_to_slack(
            f'{latest_date}\n【{ticker}】\n5日移動平均が25日移動平均を上回りました。\n買いのタイミングです。')
    elif ma5.iloc[-1] < ma25.iloc[-1]:
        send_message_to_slack(
            f'{latest_date}\n【{ticker}】\n5日移動平均が25日移動平均を下回りました。\n売りのタイミングです。', 'danger')
    check_portfolio(ticker)


if __name__ == "__main__":
    for ticker in tickers:
        check_stock(ticker)

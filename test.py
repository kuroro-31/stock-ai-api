import yfinance as yf
import datetime
import requests
import os

from tqdm import tqdm

from components.webdriver_setup import setup_driver
from components.supatrade.login import login_supatrade, new_post, new_post_send
from components.ticker_prime import tickers  # 銘柄のリストをインポート

from components.notifications import send_message_to_slack

from components.config import APP_ENV
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from components.sbi.buy import main as buy_stock


def supatrade():
    driver = setup_driver()

    try:
        login_supatrade(driver)
        new_post(driver)
        new_post_send(driver)
    except Exception as e:
        print(
            f'エラー')
        return False
    finally:
        driver.quit()


if __name__ == "__main__":
    supatrade()

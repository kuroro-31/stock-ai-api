#
# --------------------------------------------------------------------------
#  通知系の処理をまとめたファイル
# --------------------------------------------------------------------------
#
import requests
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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'


def send_message_to_slack(text):
    payload = {
        'text': text,
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    response.raise_for_status()


def send_error_to_slack(text):
    payload = {
        'attachments': [{
            'color': 'danger',  # Use 'danger' for red
            'text': text,
        }],
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    response.raise_for_status()


# 「買付余力が不足しております」
def check_insufficient_buying_power_error(driver):
    try:
        error_message_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[@class='fl01 fRed01 bold']"))
        )
        return error_message_element.text
    except TimeoutException:
        return None


# 当該注文の不足金額 (例: 1,000円)
def check_shortage_amount(driver):
    try:
        shortage_amount_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//td[@bgcolor='#ffffff' and @class='mtext-db']/div"))
        )
        return shortage_amount_element.text
    except TimeoutException:
        return None

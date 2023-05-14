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

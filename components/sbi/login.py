#
# --------------------------------------------------------------------------
#  SBI証券にログインする
# --------------------------------------------------------------------------
#
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_sbi(driver):
    driver.get('https://www.sbisec.co.jp/ETGate')

    username_value = os.getenv('SBI_USERNAME')
    password_value = os.getenv('SBI_PASSWORD')

    # ユーザーネームを入力
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "user_id"))
    )
    username.send_keys(username_value)

    # パスワードを入力
    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "user_password"))
    )
    password.send_keys(password_value)

    login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "ACT_login"))
    )
    login.click()

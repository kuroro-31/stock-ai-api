#
# --------------------------------------------------------------------------
#  住信SBIネット銀行にログインする
# --------------------------------------------------------------------------
#
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def login_sbi_bank(driver):
    driver.get(
        'https://www.netbk.co.jp/contents/pages/wpl010101/i010101CT/DI01010210')

    driver.implicitly_wait(10)

    username_value = os.getenv('SBI_BANK_USERNAME')
    password_value = os.getenv('MY_PASSWORD')

    # ユーザーネームを入力
    driver.implicitly_wait(10)
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "userNameNewLogin"))
    )
    username.send_keys(username_value)

    # パスワードを入力
    driver.implicitly_wait(10)
    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginPwdSet"))
    )
    password.send_keys(password_value)
    password.send_keys(Keys.RETURN)  # パスワード入力後にEnterキーを押します。

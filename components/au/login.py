#
# --------------------------------------------------------------------------
#  auカブコム証券にログインする
# --------------------------------------------------------------------------
#
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_au(driver):
    driver.get('https://s10.kabu.co.jp/_mem_bin/members/login.asp?/members/')

    username_value = os.getenv('AU_USERNAME')
    password_value = os.getenv('AU_PASSWORD')

    # ユーザーネームを入力
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "SsLogonUser"))
    )
    username.send_keys(username_value)

    # パスワードを入力
    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "SsLogonPassword"))
    )
    password.send_keys(password_value)

    login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "image1"))
    )
    login.click()

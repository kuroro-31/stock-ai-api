#
# --------------------------------------------------------------------------
#  LINE証券にログインする
# --------------------------------------------------------------------------
#
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_line(driver):
    driver.get('https://trade.line-sec.co.jp')

    login_page = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//a[text()="ログイン"]'))
    )
    login_page.click()

    username_value = os.getenv('LINE_USERNAME')
    password_value = os.getenv('MY_PASSWORD')

    # ユーザーネームを入力
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "tid"))
    )
    username.send_keys(username_value)

    # パスワードを入力
    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "tpasswd"))
    )
    password.send_keys(password_value)

    login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "MdBtn01"))
    )
    login.click()

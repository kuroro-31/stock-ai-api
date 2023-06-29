#
# --------------------------------------------------------------------------
#  Supatradeにログインする
# --------------------------------------------------------------------------
#
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_supatrade(driver):
    driver.get('https://www.supatrade.trade/auth/login')

    username_value = os.getenv('GOOGLE_USERNAME')
    password_value = os.getenv('SUPATRADE_PASSWORD')

    # ユーザーネームを入力
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    username.send_keys(username_value)

    # パスワードを入力
    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password.send_keys(password_value)

    login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginButton"))
    )
    login.click()


def new_post(driver):
    driver.implicitly_wait(50)
    go_newpost_page = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "new_post"))
    )
    go_newpost_page.click()


def new_post_send(driver, title, buy_message, sell_message):
    driver.implicitly_wait(50)

    content_value = buy_message + "\n --------------------- \n" + sell_message

    # ユーザーネームを入力
    title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "title"))
    )
    title.send_keys(title)

    # パスワードを入力
    content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "content"))
    )
    content.send_keys(content_value)

    send = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "submit_new_post"))
    )
    send.click()

    print("投稿完了")

#
# --------------------------------------------------------------------------
#  Googleにログインする
# --------------------------------------------------------------------------
#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from components.config import GOOGLE_USERNAME, GOOGLE_PASSWORD


def login_google(driver):
    driver.get('https://accounts.google.com')

    # Emailを入力
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'identifierId'))
    )
    email_field.send_keys(GOOGLE_USERNAME)

    # 次へボタンをクリック
    next_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'identifierNext'))
    )
    next_button.click()

    # パスワードを入力
    password_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    password_field.send_keys(GOOGLE_PASSWORD)

    # 次へボタンをクリック
    next_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'passwordNext'))
    )
    next_button.click()

#
# --------------------------------------------------------------------------
#  LINE証券にログインする
# --------------------------------------------------------------------------
#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from components.config import LINE_MAIL_ADDRESS, LINE_PASSWORD


def login_line(driver):
    driver.get('https://access.line.me/oauth2/v2.1/login?returnUri=%2Foauth2%2Fv2.1%2Fauthorize%2Fconsent%3Fredirect_uri%3Dhttps%253A%252F%252Fsso.line-sec.co.jp%252Fauth%252Fline-login%252Fauthorize%253FssoState%253D0cc4d76c1bc91647f00f13a447340648c924bf0d7ec98a8638f90fbdc7529c8f%2526serviceId%253Db1af7520-c1a5-e0b1-c727-aa93891c41ac%2526redirectUrl%253Dhttps%25253A%25252F%25252Ftrade.line-sec.co.jp%25252F%26state%3D0cc4d76c1bc91647f00f13a447340648c924bf0d7ec98a8638f90fbdc7529c8f%26client_id%3D1655651234%26response_type%3Dcode%26scope%3Dprofile%2Bopenid%26max_age%3D3600&loginChannelId=1655651234&loginState=opHxTG2nkNMJP8FoNB6V2w#/')

    username_value = LINE_MAIL_ADDRESS
    password_value = LINE_PASSWORD

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

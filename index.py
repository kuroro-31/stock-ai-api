from components.webdriver_setup import setup_driver
from components.config import APP_ENV, SBI_USERNAME, SBI_PASSWORD
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    driver = setup_driver()
    print(type(driver))

    # ブラウザの操作を行う
    driver.get('https://www.sbisec.co.jp/ETGate')

    username_value = SBI_USERNAME
    password_value = SBI_PASSWORD

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

    # 開発中でない場合は、ドライバを終了する
    if APP_ENV != 'local':
        driver.quit()

    # スクリプトが終了しないように、開発環境では無限ループを追加する
    if APP_ENV == 'local':
        while True:
            pass


if __name__ == "__main__":
    main()

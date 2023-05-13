from components.webdriver_setup import setup_driver
# from components.sbi.login import login_sbi
from components.line.login import login_line
from components.config import APP_ENV


def main():
    driver = setup_driver()

    # login_sbi(driver)  # SBI証券にログイン
    login_line(driver)  # LINE証券にログイン

    # 開発中でない場合は、ドライバを終了する
    if APP_ENV != 'local':
        driver.quit()

    # スクリプトが終了しないように、開発環境では無限ループを追加する
    if APP_ENV == 'local':
        while True:
            pass


if __name__ == "__main__":
    main()

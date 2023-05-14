#
# --------------------------------------------------------------------------
#  SeleniumとChromeDriverのセットアップ
# --------------------------------------------------------------------------
#
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def setup_driver():
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    # プロファイルパスを追加
    options.add_argument(
        "user-data-dir=/Users/st/Library/Application Support/Google/Chrome Beta/Default")

    # 環境変数からChromeとChromeDriverのパスを取得
    chrome_bin = os.getenv("GOOGLE_CHROME_BIN")
    chrome_driver_path = os.getenv("CHROMEDRIVER_PATH")

    # 環境変数が設定されている場合は、それを使用
    if chrome_bin is not None and os.getenv('APP_ENV') == 'production':
        options.binary_location = chrome_bin
        options.add_argument('--headless')
    elif os.getenv('APP_ENV') == 'local':
        options.binary_location = '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta'

    if chrome_driver_path is not None:
        driver = webdriver.Chrome(
            executable_path=chrome_driver_path, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    return driver

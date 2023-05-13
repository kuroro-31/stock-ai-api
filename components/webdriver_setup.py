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
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.binary_location = '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta' 

    # 環境変数からChromeとChromeDriverのパスを取得
    chrome_bin = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_driver_path = os.environ.get("CHROMEDRIVER_PATH")

    # 環境変数が設定されている場合は、それを使用
    if chrome_bin is not None:
        options.binary_location = chrome_bin
    if chrome_driver_path is not None:
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    return driver

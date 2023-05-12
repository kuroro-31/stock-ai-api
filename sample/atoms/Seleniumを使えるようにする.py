# 必要なライブラリをインストール
# !pip install selenium
# !apt-get update # to update ubuntu to correctly run apt install
# !apt install -y chromium-chromedriver
# !cp /usr/lib/chromium-browser/chromedriver /usr/bin

import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import os

# Chromeのオプションを設定
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# ChromeDriverのパスを指定
driver = webdriver.Chrome('chromedriver', options=chrome_options)
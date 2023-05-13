#
# --------------------------------------------------------------------------
#  SBI証券で単元未満株ページへの遷移を行う
# --------------------------------------------------------------------------
#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def navigate_to_transaction_page(driver):
    # 新規注文ページへ遷移
    transaction_page = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "img[title=取引]"))
    )
    transaction_page.click()


def navigate_to_fractional_shares_page(driver):
    # 「単元未満株」ページへ遷移
    fractional_shares_page = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//a[text()="単元未満株"]'))
    )
    fractional_shares_page.click()

#
# --------------------------------------------------------------------------
#  SBI証券のページ遷移
# --------------------------------------------------------------------------
#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from components.notifications import send_message_to_slack, send_error_to_slack, check_insufficient_buying_power_error, check_shortage_amount


# 新規注文ページへ遷移
def navigate_to_transaction_page(driver):
    driver.implicitly_wait(10)  # Add this line
    transaction_page = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "img[title=取引]"))
    )
    transaction_page.click()


# 「単元未満株」ページへ遷移
def navigate_to_fractional_shares_page(driver):
    driver.implicitly_wait(30)  # Add this line
    fractional_shares_page = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//a[text()="単元未満株"]'))
    )
    fractional_shares_page.click()


# 単元未満株のフォームを埋める
def fill_form(driver, ticker, purchase_number):
    # '取引'を'現物買'に選択
    trade_radio_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "genK"))
    )
    trade_radio_button.click()

    stock_sec_code_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "stock_sec_code"))
    )
    stock_sec_code_field.clear()
    # '銘柄コード'に指定したtickerを入力
    stock_sec_code_field.send_keys(ticker)

    # '株数'に'1'を入力
    quantity_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "input_quantity"))
    )
    quantity_field.clear()
    quantity_field.send_keys(purchase_number)

    # '預り区分'を'特定預り'に選択
    deposit_radio_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//input[@name="hitokutei_trade_kbn" and @value="0"]'))
    )
    deposit_radio_button.click()


# 「（S株）取引ルール（基準となる市場及び取引時間等）に同意する」にチェックを入れる
def agree_to_rules(driver):
    agreement_checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "odd_agreement"))
    )
    agreement_checkbox.click()


# 「取引パスワード」の入力
def input_password(driver, password):
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "trade_pwd"))
    )
    password_field.clear()
    password_field.send_keys(password)


# 「注文確認画面へ」のクリック
def click_order_confirmation(driver):
    order_confirmation_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='注文確認画面へ']"))
    )
    order_confirmation_button.click()
    error_message = check_insufficient_buying_power_error(driver)
    shortage_amount = check_shortage_amount(driver)  # 不足金額を取得
    if error_message and shortage_amount:
        send_error_to_slack(error_message + "\n不足金額: " +
                            shortage_amount)  # エラーメッセージと不足金額を一緒に送信


# 「注文発注」のクリック
def click_order_place(driver):
    driver.implicitly_wait(50)
    order_place_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='注文発注']"))
    )
    order_place_button.click()

    send_message_to_slack('購入が完了しました。\n翌営業日から保有銘柄に追加されます。')

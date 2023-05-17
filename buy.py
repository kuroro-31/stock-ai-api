#
# --------------------------------------------------------------------------
#  現物1株の自動売買スクリプト
# --------------------------------------------------------------------------
#
import os
from components.webdriver_setup import setup_driver
from components.sbi.login import login_sbi
from components.config import APP_ENV
from components.sbi.navigation import navigate_to_transaction_page, navigate_to_fractional_shares_page, fill_form, agree_to_rules, input_password, click_order_confirmation, click_order_place


def main():
    driver = setup_driver()

    login_sbi(driver)  # SBI証券にログイン

    navigate_to_transaction_page(driver)  # 「取引」ページへ遷移
    navigate_to_fractional_shares_page(driver)  # 「単元未満株」ページへ遷移
    fill_form(driver)  # 単元未満株のフォームを埋める
    agree_to_rules(driver)  # 「（S株）取引ルール（基準となる市場及び取引時間等）に同意する」にチェックを入れる
    input_password(driver, os.getenv('MY_PASSWORD'))  # 「取引パスワード」の入力
    click_order_confirmation(driver)  # 「注文確認画面へ」のクリック
    click_order_place(driver)  # 「注文発注」のクリック

    # 開発中でない場合は、ドライバを終了する
    if os.getenv('APP_ENV') != 'local':
        driver.quit()

    # スクリプトが終了しないように、開発環境では無限ループを追加する
    if os.getenv('APP_ENV') == 'local':
        while True:
            pass


if __name__ == "__main__":
    main()

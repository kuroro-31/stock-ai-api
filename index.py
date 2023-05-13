from components.webdriver_setup import setup_driver
from components.config import SBI_USERNAME, SBI_PASSWORD


def main():
    driver = setup_driver()

    # ブラウザの操作を行う
    driver.get('https://www.sbisec.co.jp/ETGate')

    username_value = SBI_USERNAME
    password_value = SBI_PASSWORD

    username = driver.find_element_by_name("user_id")
    username.send_keys(username_value)

    password = driver.find_element_by_name("user_password")
    password.send_keys(password_value)

    driver.quit()


if __name__ == "__main__":
    main()

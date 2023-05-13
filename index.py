from components.webdriver_setup import setup_driver
from components.config import SBI_USERNAME, SBI_PASSWORD

def main():
    driver = setup_driver()

    # ブラウザの操作を行う
    driver.get('https://www.google.com')
    print(driver.title)

    driver.quit()

if __name__ == "__main__":
    main()
#
# --------------------------------------------------------------------------
#  envファイルから環境変数を読み込む
# --------------------------------------------------------------------------
#
from dotenv import load_dotenv
import os

load_dotenv()

APP_ENV = os.getenv('APP_ENV')
SBI_USERNAME = os.environ.get('SBI_USERNAME')
SBI_PASSWORD = os.environ.get('SBI_PASSWORD')
LINE_USERNAME = os.environ.get('LINE_USERNAME')
LINE_PASSWORD = os.environ.get('LINE_PASSWORD')
AU_USERNAME = os.environ.get('AU_USERNAME')
AU_PASSWORD = os.environ.get('AU_PASSWORD')

import yfinance as yf
import datetime
import requests
import os

from components.tickers import tickers  # 銘柄のリストをインポート

os.environ['SLACK_WEBHOOK_URL'] = 'https://hooks.slack.com/services/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'


def get_stock_data(ticker):
    end = datetime.datetime.now()
    # 60日前のデータを取得します (週末や祝日を考慮して余裕を持たせています)
    start = end - datetime.timedelta(days=60)
    df = yf.download(ticker, start, end)
    return df, end.strftime('%Y年%m月%d日')  # 最新のデータ日を返す


def calculate_moving_averages(df):
    ma5 = df['Close'].rolling(window=5).mean()  # 5日移動平均
    ma25 = df['Close'].rolling(window=25).mean()  # 25日移動平均
    return ma5, ma25


def send_message_to_slack(text, action):
    print(f'Sending message to slack: {text}')
    color = 'good' if action == 'buy' else 'danger'  # 買いの場合は青色、売りの場合は赤色
    payload = {
        'attachments': [{
            'color': color,
            'text': text,
        }],
    }
    response = requests.post(os.getenv('SLACK_WEBHOOK_URL'), json=payload)
    response.raise_for_status()


def check_stock(ticker):
    df, latest_date = get_stock_data(ticker)  # 最新のデータ日を取得
    ma5, ma25 = calculate_moving_averages(df)

    print(f'5-day MA: {ma5.iloc[-1]}, 25-day MA: {ma25.iloc[-1]}')

    if ma5.iloc[-1] > ma25.iloc[-1]:
        send_message_to_slack(
            f'{latest_date}\n【{ticker}】\n5日移動平均が25日移動平均を上回りました。\n買いのタイミングです。', 'buy')
    elif ma5.iloc[-1] < ma25.iloc[-1]:
        send_message_to_slack(
            f'{latest_date}\n【{ticker}】\n5日移動平均が25日移動平均を下回りました。\n売りのタイミングです。', 'sell')


if __name__ == "__main__":
    for ticker in tickers:
        check_stock(ticker)

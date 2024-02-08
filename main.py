import configparser
import requests
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass

def movingAverageCrossover(sma, lma):
    buySignal = sma - lma
    sellSignal = lma - sma
    return buySignal, sellSignal


config = configparser.ConfigParser()
config.read('config.ini')

API_KEY_ID = config['alpaca']['paper_key_id']
API_SECRET_KEY = config['alpaca']['paper_secret_key']
BASE_URL = 'https://paper-api.alpaca.markets'

url = "https://data.alpaca.markets/v2/stocks/AAPL/bars?timeframe=1D&start=2022-01-03T00%3A00%3A00Z&limit=1000&adjustment=raw&feed=sip&sort=asc"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "APCA-API-KEY-ID": API_KEY_ID,
    "APCA-API-SECRET-KEY": API_SECRET_KEY
    }

api = TradingClient(API_KEY_ID, API_SECRET_KEY, paper=True)
account = api.get_account()
cash = float(account.cash)

search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
assets = api.get_all_assets(search_params)


response = requests.get(url, headers=headers).json()
response = response['bars']

closing_prices = []
for bar in response:
    closing_prices.append(bar['c'])

short_period = 50
long_period = 200

sma = sum(closing_prices[-short_period:]) / short_period
lma = sum(closing_prices[-long_period:]) / long_period

signal = movingAverageCrossover(sma, lma)

order_url = 'https://paper-api.alpaca.markets/v2/orders'


if(signal[0] > 0):
    side="buy"
else:
    side="sell"

if(signal[0] > 5 or signal[1] > 5):
    notional = cash * .1
else:
    notional = cash * .05

payload = {
    "side": side,
    "type": "market",
    "time_in_force": "day",
    "symbol": "AAPL",
    "notional": notional
}

response = requests.post(order_url, json=payload, headers=headers)
print(response.text)
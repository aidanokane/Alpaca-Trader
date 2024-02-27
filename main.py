import configparser
import requests
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass

def movingAverageCrossover (short_period, long_period, closing_prices, cash,
                            buyThresholds, sellThresholds, amounts):
    sma = sum(closing_prices[-short_period:]) / short_period
    lma = sum(closing_prices) / long_period
    buySignal = sma/lma
    sellSignal = lma/sma

    if(buySignal > 0):
        side="buy"
    else:
        side="sell"

    if(buySignal > buyThresholds[0]):
        notional = cash * amounts[0]
    elif(sellSignal > sellThresholds[0]):
        notional = cash * amounts[0]
    elif(buySignal > buyThresholds[1]):
        notional = cash * amounts[1]
    elif(sellSignal > sellThresholds[1]):
        notional = cash * amounts[1]
    else:
        notional = 0
        
    return side, notional

def main():
    config = configparser.ConfigParser()
    config.read('.gitignore/config.ini')

    SYMBOLS = [
        "AAPL", "ADBE", "AMZN", "GOOGL", "XOM",
        "INTC", "MSFT", "MAR", "NVDA", "VOO"]
    
    API_KEY_ID = config['alpaca']['paper_key_id']
    API_SECRET_KEY = config['alpaca']['paper_secret_key']
    BASE_URL = 'https://paper-api.alpaca.markets'

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "APCA-API-KEY-ID": API_KEY_ID,
        "APCA-API-SECRET-KEY": API_SECRET_KEY
        }

    api = TradingClient(API_KEY_ID, API_SECRET_KEY, paper=True)
    account = api.get_account()

    search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
    assets = api.get_all_assets(search_params)
    cash = float(account.cash)

    for symbol in SYMBOLS:
        
        print(cash)
        url = f"https://data.alpaca.markets/v2/stocks/{symbol}/bars?timeframe=1D&start=2022-01-03T00%3A00%3A00Z&limit=1000&adjustment=raw&feed=sip&sort=asc"
        response = requests.get(url, headers=headers).json()
        response = response['bars']

        closing_prices = []
        for bar in response:
            closing_prices.append(bar['c'])

        short_period = 50
        long_period = 200
        
        signal = movingAverageCrossover(short_period, long_period, closing_prices, cash, [1.1, 1.02], [1.1, 1.02], [.1, .05])

        order_url = 'https://paper-api.alpaca.markets/v2/orders'

        payload = {
            "side": signal[0],
            "type": "market",
            "time_in_force": "day",
            "symbol": symbol,
            "notional": "{:.2f}".format(signal[1])
        }
        if(signal[0] == 'buy'):
            cash -= signal[1]
        else:
            cash += signal[1]

        response = requests.post(order_url, json=payload, headers=headers)
        print(response.text)

if __name__ == "__main__":
    main()
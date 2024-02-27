import configparser
import vectorbt as vbt

def initializeClosingData():
    stocks = [
            "AAPL", "ADBE", "AMZN", "GOOGL", "XOM",
            "INTC", "MSFT", "MAR", "NVDA"]
    config = configparser.ConfigParser()
    config.read('.gitignore/config.ini')

    API_KEY_ID = config['alpaca']['paper_key_id']
    API_SECRET_KEY = config['alpaca']['paper_secret_key']

    vbt.settings.data['alpaca']['key_id'] = API_KEY_ID
    vbt.settings.data['alpaca']['secret_key'] = API_SECRET_KEY

    closingData = []

    for i in range(len(stocks)):
        alpacaData = vbt.AlpacaData.download(
            symbols=stocks[i],
            start='300 days ago UTC',
            end='1 days ago UTC',
            interval='1d'
        )
        closingData.append(alpacaData.get()['Close'].values)
    return closingData
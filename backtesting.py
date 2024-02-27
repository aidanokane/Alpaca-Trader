import vectorbt as vbt
import configparser
from main import movingAverageCrossover as ma

stocks = [
        "AAPL", "ADBE", "AMZN", "GOOGL", "XOM",
        "INTC", "MSFT", "MAR", "NVDA"]

def main():
    config = configparser.ConfigParser()
    config.read('.gitignore/config.ini')

    API_KEY_ID = config['alpaca']['paper_key_id']
    API_SECRET_KEY = config['alpaca']['paper_secret_key']

    vbt.settings.data['alpaca']['key_id'] = API_KEY_ID
    vbt.settings.data['alpaca']['secret_key'] = API_SECRET_KEY

    short_period = 5
    long_period = 10

    closingData = []

    for i in range(len(stocks)):
        short_period = 5
        long_period = 1
        cash = 100000
        buyThresholds = [0.0015484396229900402, 0.017313850414689635]
        sellThresholds = [0.0006384816593047768, 0.0002147111661641745]
        amounts = [0.0009589894223510509, 0.00019284972205218463]
        alpacaData = vbt.AlpacaData.download(
            symbols=stocks[i],
            start='300 days ago UTC',
            end='1 days ago UTC',
            interval='1d'
        )

        closingData.append(alpacaData.get()['Close'].values)
    print(backtesting(closingData, short_period, long_period, cash, buyThresholds, sellThresholds, amounts))

def backtesting(closingData, short_period, long_period, cash, buyThresholds, sellThresholds, amounts):
    cash = 100000

    quant = []
    for stock in stocks:
        quant.append(0)

    for x in range(long_period, len(closingData[0])):
            for y in range(len(closingData)):
                frame = closingData[y][(x-long_period):x]
                signals = ma(short_period, long_period, frame, cash, buyThresholds, sellThresholds, amounts)

                #Logic for buying the stock
                if(signals[0] == 'buy' and cash - signals[1] > 0):
                    cash -= signals[1]
                    quant[y] += (signals[1] / closingData[y][x])
                    #print("BUY:", stocks[y], ",", (signals[1] / closingData[y][x]))
                elif(signals[1] == 'sell' and quant - (signals[1] / closingData[y][x]) > 0):
                    cash += signals[1]
                    quant[y] -= (signals[1] / closingData[y][x])
                    #print("SELL:", stocks[y], ",", (signals[1] / closingData[y][x]))

    #print(len(closingData[0]))

    pf = cash
    for i in range(len(quant)):
        pf += (quant[i] * closingData[i][-1])

    return(pf)


if __name__ == '__main__':
    main()
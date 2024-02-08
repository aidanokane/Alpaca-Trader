import vectorbt as vbt
import configparser
from main import movingAverageCrossover as ma

list = [
    "AAPL", "ADBE", "AMZN", "GOOGL", "XOM",
    "INTC", "MSFT", "MAR", "NVDA"]

config = configparser.ConfigParser()
config.read('.gitignore/config.ini')

API_KEY_ID = config['alpaca']['paper_key_id']
API_SECRET_KEY = config['alpaca']['paper_secret_key']

vbt.settings.data['alpaca']['key_id'] = API_KEY_ID
vbt.settings.data['alpaca']['secret_key'] = API_SECRET_KEY

closingData = []

for i in range(len(list)):
    alpacaData = vbt.AlpacaData.download(
        symbols=list[i],
        start='725 days ago UTC',
        end='1 days ago UTC',
        interval='1d'
    )

    closingData.append(alpacaData.get()['Close'].values)
print(alpacaData.get()['Close'].keys)

cash = 100000
quant = [0, 0, 0, 0, 0, 0, 0, 0, 0]
short_period = 5
long_period = 10

for x in range(long_period, len(closingData[0])):
        for y in range(len(closingData)):
            frame = closingData[y][(x-long_period):x]
            signals = ma(short_period, long_period, frame, cash, quant[y])

            #Logic for buying the stock
            if(signals[0] == 'buy' and cash - signals[1] > 0):
                cash -= signals[1]
                quant[y] += (signals[1] / closingData[y][x])
                print("BUY:", list[y], ",", quant[y])
            elif(signals[1] == 'sell' and quant - (signals[1] / closingData[y][x]) > 0):
                cash += signals[1]
                quant[y] -= (signals[1] / closingData[y][x])
                print("SELL:", list[y], ",", quant[y])

print(len(closingData[0]))

pf = cash
for i in range(len(quant)):
    print(f"{list[i]}: {quant[i]} shares (${quant[i] * closingData[i][-1]})")
    pf += (quant[i] * closingData[i][-1])
print(f"${cash}, free cash")

print(pf)
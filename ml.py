from TradingThread import TradingThread
from Instance import Instance
from backtesting import backtesting
from init import initializeClosingData

closingData = initializeClosingData()

def generation(numThreads, values):
    threads = []
    for i in range(numThreads):
        thread = TradingThread(values)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    elite = [thread.elite for thread in threads]
    elite = sorted(elite, key=lambda x: x.balance)
    return elite[-1]


def main():
    numGenerations = 100
    numThreads = 100
    values = [closingData, 5, 10, [1.1, 1.02], [1.1, 1.02], [.1, .05]]
    instance = Instance(values)
    instance.simulate()
    balanceHigh = instance.balance
    print(balanceHigh)
    for i in range(numGenerations):
        #run the generation
        elite = generation(numThreads, values)
        if(balanceHigh < elite.balance):
            values = elite.getValues()
            balanceHigh = elite.balance
        print(elite.balance)

    print(values[1:])
        
if __name__ == "__main__":
    main()
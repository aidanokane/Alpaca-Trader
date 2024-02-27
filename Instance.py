from backtesting import backtesting
import random

class Instance:
    
    def __init__(self, values):
        self.closingData = values[0]
        self.shortPeriod = values[1]
        self.longPeriod = values[2]
        self.buyThresholds = values[3]
        self.sellThresholds = values[4]
        self.amounts = values[5]
        self.balance = 0

    def simulate(self):
        cash = 100000
        self.balance = backtesting(self.closingData, self.shortPeriod,
                                    self.longPeriod, cash, self.buyThresholds,
                                    self.sellThresholds, self.amounts)

    def mutate(self):
        self.shortPeriod = random.choice([self.shortPeriod - 1, self.shortPeriod, self.shortPeriod + 1])
        if(self.shortPeriod < 1): 
            self.shortPeriod = 1
        self.longPeriod = random.choice([self.longPeriod - 1, self.longPeriod, self.longPeriod + 1])
        if(self.longPeriod < 1):
            self.longPeriod = 1
        self.buyThresholds[0] *= random.uniform(.9, 1.1)
        self.buyThresholds[1] *= random.uniform(.9, 1.1)
        self.sellThresholds[0] *= random.uniform(.9, 1.1)
        self.sellThresholds[1] *= random.uniform(.9, 1.1)
        self.amounts[0] *= random.uniform(.9, 1.1)
        self.amounts[1] *= random.uniform(.9, 1.1)

    
    def getBalance(self):
        return self.balance
    
    def getValues(self):
        return([self.closingData, self.shortPeriod, self.longPeriod,
                    self.buyThresholds, self.sellThresholds, self.amounts])

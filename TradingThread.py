import threading
from Instance import Instance

class TradingThread(threading.Thread):
    def __init__(self, values):
        super().__init__()
        self.values = values
        self.elite = Instance(self.values)

    def run(self):
        instance = Instance(self.values)
        instance.mutate()
        instance.simulate()
        self.elite = instance


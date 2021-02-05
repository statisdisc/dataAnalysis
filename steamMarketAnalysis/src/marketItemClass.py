import numpy as np

#Object to store all important information for item on the market
class marketItem:
    def __init__(self, name):
        self.name = name
        
        #Historic data of sales on market
        self.dates = np.array([0])
        self.timestamps = np.array([0])
        self.prices = np.array([0])
        self.quantities = np.array([0])
    
    def timeReleased(self):
        return np.min(self.timestamps)
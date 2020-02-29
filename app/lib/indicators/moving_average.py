import numpy as np
import Db
import Api

class MovingAverage(object):
    def __init__(self, market, data, range):
        self.market_data = data
        self.price_data = Db.get_price_history(market, range)
        self.range = range
        self.__check_data_length()

    def sma(self):
        return np.sum(self.price_data[len(self.price_data) - self.range:]) / self.range
    
    def ema(self):
        multiplier = 2 / (self.range + 1)
        # TODO: figure out the best way to store prev_ema. probs in db
        prev_ema = self.market_data['indicator'][f'ema_{self.range}']
        if prev_ema is 0:
            prev_ema = self.sma()
        return self.price_data[-1] * multiplier + prev_ema * (1 - multiplier)

    def __check_data_length(self):
        if self.range > len(self.price_data):
            Api.get_price_history()



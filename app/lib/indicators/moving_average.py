import numpy as np
from app.lib.common.mysql import Db
from app.lib.common.exchange_api import Api


class MovingAverage(object):
    def __init__(self, market, data, limit):
        self.market = market
        self.market_data = data
        self.price_data = Db().get_price_history(market, limit)
        self.limit = limit
        self.__check_data_length()

    def sma(self):
        prices = []
        for row in self.price_data:
            prices.append(float(row[0]))
        return np.sum(prices) / float(self.limit)

    def ema(self):
        multiplier = 2.0 / (self.limit + 1.0)
        # TODO: figure out the best way to store prev_ema. probs in db
        prev_ema = self.market_data['indicator'][f'ema_{self.limit}']
        if prev_ema == 0.0:
            prev_ema = self.sma()
        return float(self.price_data[0][0]) * multiplier + prev_ema * (1.0 - multiplier)

    def __check_data_length(self):
        db = Db()
        if self.limit > len(self.price_data):
            candle_history = Api().get_candle_history(self.market, self.limit)
            for interval in candle_history:
                db.add_price(
                    self.market, interval[4], interval[4], interval[4])
            self.price_data = db.get_price_history(self.market, self.limit)

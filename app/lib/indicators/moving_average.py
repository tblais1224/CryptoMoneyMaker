import numpy as np


class MovingAverage(object):
    def __init__(self, price_data):
        self.price_data = price_data

    def sma(self, range):
        if self.__check_data_length(range) == 0:
            return
        return np.sum(self.price_data[len(self.price_data) - range:]) / range

    def ema(self, range, prev_ema=None):
        if self.__check_data_length(range + 1) == 0:
            return
        multiplier = 2 / (range + 1)
        if prev_ema is None:
            prev_ema = self.sma(range)
        return self.price_data[-1] * multiplier + prev_ema * (1 - multiplier)

    def __check_data_length(self, length):
        if range > len(self.price_data):
            print('Not enough data given for this range.')
            return 0


# def moving_average_list(values, window):
#     weights = np.repeat(1.0, window)/window
#     smas = np.convolve(values,weights,'valid')
#     return smas

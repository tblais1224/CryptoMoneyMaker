import numpy as np


class MovingAverage(object):
    def __init__(self, price_data):
        self.price_data = price_data

    def sma(self, range):
        if self.__check_data_range(range) == 0: return
        return np.sum(self.price_data[len(self.price_data) - range:])/range

    def ema(self, range):
        pass

    def __check_data_range(self, range):
        if range > len(self.price_data):
            print('Not enough data given for this range.')
            return 0



# def moving_average_list(values, window):
#     weights = np.repeat(1.0, window)/window
#     smas = np.convolve(values,weights,'valid')
#     return smas
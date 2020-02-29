import numpy as np
from indicators import MovingAverage

class MultiEma(MovingAverage):
    def buy(self, parameter_list):
      pass


# def moving_average_list(values, window):
#     weights = np.repeat(1.0, window)/window
#     smas = np.convolve(values,weights,'valid')
#     return smas

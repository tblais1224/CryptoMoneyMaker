import numpy as np
import json
from config.bittrex import BITTREX
from app.lib.moving_average import MovingAverage
from bittrex.bittrex import Bittrex
import matplotlib.pyplot as plt
import pandas as pd

# or defaulting to v1.1 as Bittrex(None, None)
my_bittrex = Bittrex(BITTREX['api_key'], BITTREX['api_secret'])
# print(my_bittrex.get_market_summary('USD-BTC'))

# api endpoint https://api.bittrex.com/api/v1.1

data = [3, 6, 7, 4, 1]

# use close price for moving avg


def moving_average_test(values, window):
    weights = np.repeat(1.0, window)/window
    smas = np.convolve(values, weights, 'valid')
    return smas


print('test sma')
print(moving_average_test(data, 4))

print('class sma')
print(MovingAverage(data).sma(4))

# 8, 13, 21, 55  moving avgs   update 3 or 5 min maybe to start

with open('btc_data.json') as f:
    btc_data = json.load(f)

btc_close_prices = []
btc_date = []

for interval in btc_data['result'][:1000]:
    btc_close_prices.append(interval['C'])
    btc_date.append(btc_data['result'].index(interval))


print(moving_average_test(btc_close_prices, 55))

print('btc hist sma')
print(MovingAverage(btc_close_prices).sma(55))

plt.plot(btc_date, btc_close_prices, label='BTC-USD')


sma_8 = btc_close_prices.rolling(window=8).mean()
sma_13 = btc_close_prices.rolling(window=13).mean()
sma_21 = btc_close_prices.rolling(window=21).mean()
sma_55 = btc_close_prices.rolling(window=55).mean()

plt.plot(btc_date, sma_8, label='AMD 8 MIN SMA', color='orange')
plt.plot(btc_date, sma_13, label='AMD 13 MIN SMA', color='magenta')
plt.plot(btc_date, sma_21, label='AMD 13 MIN SMA', color='magenta')
plt.plot(btc_date, sma_55, label='AMD 13 MIN SMA', color='magenta')

plt.legend(loc='upper left')
plt.show()

plt.show()
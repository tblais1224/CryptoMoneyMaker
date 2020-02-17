import numpy as np
from config.bittrex import BITTREX
from app.lib.moving_average import MovingAverage
from bittrex.bittrex import Bittrex
import btc_data

# or defaulting to v1.1 as Bittrex(None, None)
my_bittrex = Bittrex(BITTREX['api_key'], BITTREX['api_secret'])
# print(my_bittrex.get_market_summary('USD-BTC'))

# api endpoint https://api.bittrex.com/api/v1.1

data = [3, 6, 7, 4, 1]

# use close price for moving avg
def moving_average_test(values, window):
    weights = np.repeat(1.0, window)/window
    smas = np.convolve(values,weights,'valid')
    return smas

print('test sma')
print(moving_average_test(data, 4))

sma = MovingAverage(data)

print('class sma')
print(sma.sma(6))

# 8, 13, 21, 55  moving avgs   update 3 or 5 min maybe to start

import json
with open('path_to_file/person.json') as f:
  data = json.load(f)
# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
print(data)
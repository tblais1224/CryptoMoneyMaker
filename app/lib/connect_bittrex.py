import numpy as np
import json
import time
from config.bittrex import BITTREX
from app.lib.moving_average import MovingAverage
from bittrex.bittrex import Bittrex


buying_power = 1000
holding = 0
prev_buy_price = 1
prev_btc_price = 1
buy = False
sell = False

prev_prices = [
    9797.27581818, 9797.769, 9798.15625455, 9798.58089091, 9799.00767273, 9799.26152727, 9799.50316364, 9799.9438, 9800.42654545, 9800.60192727, 9800.9262, 9801.15843636, 9801.46432727, 9801.72814545, 9801.97952727, 9802.28318182, 9802.72996364, 9803.15478182, 9804.08023636, 10176.074, 10176.074, 10176.074, 10176.074, 10176.074, 10176.074, 10176.074, 10176.074, 10176.074, 10176.074, 10176.074, 10176.074, 10176.074, 10176.074, 10176.074, 10176.074
]

markets = {
    'bitcoin': {
        'market': 'BTC-USD',
        'prev_prices': [],
        'buy': False,
        'sell': True,
        'holding_usd': 0
    },
    'tezos': {
        'market': 'XTZ-USD',
        'prev_prices': [],
        'buy': False,
        'sell': True,
        'holding_usd': 0
    },
    'litecoin': {
        'market': 'LTC-USD',
        'prev_prices': [],
        'buy': False,
        'sell': True,
        'holding_usd': 0
    },
    'ethereum': {
        'market': 'ETH-USD',
        'prev_prices': [],
        'buy': False,
        'sell': True,
        'holding_usd': 0
    },
    'bitcoin cash': {
        'market': 'BCH-USD',
        'prev_prices': [],
        'buy': False,
        'sell': True,
        'holding_usd': 0
    },
    'xrp': {
        'market': 'XRP-USD',
        'prev_prices': [],
        'buy': False,
        'sell': True,
        'holding_usd': 0
    },
    'bitcoin sv': {
        'market': 'BSV-USD',
        'prev_prices': [],
        'buy': False,
        'sell': True,
        'holding_usd': 0
    }
}

# or defaulting to v1.1 as Bittrex(None, None)
my_bittrex = Bittrex(BITTREX['api_key'], BITTREX['api_secret'])
print(my_bittrex.get_market_summary('USD-BTC'))

# api endpoint https://api.bittrex.com/api/v1.1

# 8, 13, 21, 55  moving avgs   update 3 or 5 min maybe to start


starttime = time.time()

while True:
    api_result = my_bittrex.get_market_summary('USD-BTC')['result'][0]
    bid_ask_avg = (api_result['Ask'] + api_result['Bid']) / 2
    if len(prev_prices) > 21:
        prev_prices.pop(0)
    prev_prices.append(bid_ask_avg)

    ma_intervals = [21, 13, 8]
    if len(prev_prices) >= 21:
        prev_sma = 0
        for interval in ma_intervals:
            ma = MovingAverage(prev_prices)
            sma = ma.sma(interval)
            print('prev_sma {}, sma {}'.format(prev_sma, sma))
            if prev_sma < sma:
                buy = True
                sell = False
            else:
                buy = False
                sell = True
                break
            prev_sma = sma

    percent_change_price = bid_ask_avg / prev_btc_price
    holding = holding * percent_change_price

    if buy == True and sell == False and holding == 0:
        holding = buying_power
        buying_power = 0
        prev_buy_price = bid_ask_avg
    elif buy == False and sell == True:
        buying_power += holding
        holding = 0

    print("bid ask avg: {}, prev btc price: {}\nbuy: {}, sell: {}\nholding: {}, buy_power: {}\n".format(
        bid_ask_avg, prev_btc_price, buy, sell, holding, buying_power))

    prev_btc_price = bid_ask_avg
    time.sleep(5.0 - ((time.time() - starttime) % 5.0))

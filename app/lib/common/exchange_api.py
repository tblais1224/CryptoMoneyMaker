from config.config_info import API
from .mysql import Db
import requests
import sys
sys.path.append('/home/tom/Documents/CodingProjects/CryptoBot')


class Api(object):
    def __init__(self, exchange='binance'):
        self.exchange = exchange
        self.signature = API[exchange]['api_secret']
        self.base_url = API[exchange]['base_endpoint']
        self.payload = {}
        self.headers = {
            'Content-Type': 'application/json',
            'X-MBX-APIKEY': API['binance']['api_key']
        }
        self.recvWindow = 2500

    def get_market_price(self, market=None):
        url = f'{self.base_url}ticker/bookTicker'
        if market:
            self.payload = {
                'symbol': market
            }
        return requests.request("GET", url, headers=self.headers, params=self.payload).json()

    def get_candle_history(self, market, limit, interval='1m'):
        url = f'{self.base_url}klines'
        self.payload = {
            'symbol': market,
            'limit': limit,
            'interval': interval
        }
        return requests.request("GET", url, headers=self.headers, params=self.payload).json()


# def get_market_history(self, market):c
#     params = {
#         'symbol': market
#     }
#     response = requests.request("GET", url, headers=headers, data = payload)

#     print(response.text.encode('utf8'))
# return requests.get('{self.api_path}/api/v3/ticker/bookTicker', params=params).json()

# params = {
#     'symbol': 'LTCUSDT'
# }
# response = requests.get(f'{binance}/api/v3/ticker/bookTicker', params=params)
# print(response.json())

# https://api.binance.com

# A SIGNED endpoint also requires a parameter, timestamp, to be sent which should be the millisecond timestamp of when the request was created and sent.
# An additional parameter, recvWindow, may be sent to specify the number of milliseconds after timestamp the request is valid for. If recvWindow is not sent, it defaults to 5000.
# reject requests that go over time limit

# if timestamp < (serverTime + 1000) and (serverTime - timestamp) <= recvWindow:
#     print(response)
# else:
#     print('request too too long to complete')

from config import config_info
from .mysql import Db
import requests
import sys
sys.path.append('/home/tom/Documents/CodingProjects/CryptoBot')


class Api(object):
    def __init__(self, exchange):
        self.exchange = exchange
        self.api_path = config_info.API[exchange]['base_endpoint']
        self.key = config_info.API[exchange]['api_key']
        self.secret = config_info.API[exchange]['api_secret']
        self.url = ""
        self.payload = {}
        self.headers= {}

    def get_market_price(self, market=None):
        if market is None:
            return requests.get(f'{self.api_path}/api/v3/ticker/bookTicker').json()
        params = {
            'symbol': market
        }
        return requests.get(f'{self.api_path}/api/v3/ticker/bookTicker', params=params).json()

    def get_market_history(self, market):
        params = {
            'symbol': market
        }
        response = requests.request("GET", url, headers=headers, data = payload)

        print(response.text.encode('utf8'))
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

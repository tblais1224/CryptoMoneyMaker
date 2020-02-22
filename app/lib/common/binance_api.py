import sys  
sys.path.append('/home/tom/Documents/CodingProjects/CryptoBot')  
import requests
from config import config_info

binance = config_info.BINANCE['base_endpoint']

params = {
    'symbol': 'XRPUSDT'
}

response = requests.get(f'{binance}/api/v3/ticker/bookTicker', params=params)
print(response.json())

# https://api.binance.com

# A SIGNED endpoint also requires a parameter, timestamp, to be sent which should be the millisecond timestamp of when the request was created and sent.
# An additional parameter, recvWindow, may be sent to specify the number of milliseconds after timestamp the request is valid for. If recvWindow is not sent, it defaults to 5000.
# reject requests that go over time limit

# if timestamp < (serverTime + 1000) and (serverTime - timestamp) <= recvWindow:
#     print(response)
# else:
#     print('request too too long to complete')

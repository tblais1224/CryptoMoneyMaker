import requests
import time
from config.config_info import API

# must be in milli s
timestamp = time.time() * 1000

# default is 5000 milli s
recvWindow = 2000

signature = API['binance']['api_secret']

url = f'https://api.binance.com/api/v3/order/test?symbol=BTCUSDT&side=SELL&type=LIMIT&timeInForce=GTC&quantity=0.01&price=9000&newClientOrderId=my_order_id_1&timestamp={timestamp}&signature={signature}&recvWindow={recvWindow}'

payload = {}
headers = {
    'Content-Type': 'application/json',
    'X-MBX-APIKEY': API['binance']['api_key']
}

response = requests.request("POST", url, headers=headers, data=payload)

serverTime = response.elapsed.total_seconds() + timestamp

print(timestamp, serverTime)

if timestamp < (serverTime + 1000) and (serverTime - timestamp) <= recvWindow:
    print(response.text.encode('utf8'))
else:
    print('request took too long to complete')

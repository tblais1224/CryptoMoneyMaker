from app.lib.common import exchange_api, mysql, graphing
import sys, time, signal
sys.path.append('/home/tom/Documents/CodingProjects/CryptoBot')

starttime = time.time()

timeout = 5.0
loop_count = 0
run = True
market = 'LTCUSDT'
api = exchange_api.Api('binance')
db = mysql.Db('crypto_bot')

def signal_handler(signal, frame):
    global run
    print('\nSTOPPING BOT')
    run = False

signal.signal(signal.SIGINT, signal_handler)

while run:
    loop_count += 1
    price_data = api.get_market_price(market)
    bid = float(price_data['bidPrice'])
    ask = float(price_data['askPrice'])
    bid_ask_avg = (bid+ask)/2
    print(f'market: {market}, bid ask avg: {bid_ask_avg}, bid: {bid}, ask: {ask}')
    db.add_price(market, bid_ask_avg, bid, ask)
    print(f'Bot run count: {loop_count} done, continuing in {timeout} seconds...')
    print('Press CTRL+c to sell off all coins and stop bot...\n')
    time.sleep(timeout)
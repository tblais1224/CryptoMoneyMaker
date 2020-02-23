from app.lib.common import exchange_api, mysql, graphing
from app.data import markets
import sys, time, signal
sys.path.append('/home/tom/Documents/CodingProjects/CryptoBot')

time_interval = 5.0

loop_count = 0
run = True

api = exchange_api.Api('binance')
db = mysql.Db('crypto_bot')

def signal_handler(signal, frame):
    global run
    print('\nSTOPPING BOT')
    run = False

signal.signal(signal.SIGINT, signal_handler)

# check current wallet and set values in markets
buying_power_coin = 'USDT'
buying_power_amount = 1000

while run:
    loop_count += 1
    all_market_data = api.get_market_price()

    for market in all_market_data:
        symbol = market['symbol']
        if markets.MARKETS.get(symbol, None) != None and markets.MARKETS[symbol]['trade'] == True:
            bid = float(market['bidPrice'])
            ask = float(market['askPrice'])
            bid_ask_avg = (bid+ask)/2
            markets.MARKETS['last_price'] = bid_ask_avg

            strategy_check = multi_ema(symbol, bid_ask_avg).buy_or_sell()
            if strategy_check == 'buy':
                
            elif strategy_check == 'sell':

            db.add_price(symbol, bid_ask_avg, bid, ask)
            print(f'market: {symbol}, bid ask avg: {bid_ask_avg}, bid: {bid}, ask: {ask}')


    print(f'Bot run count: {loop_count} done, continuing in {time_interval} seconds...')
    print('Press CTRL+c to sell off all coins and stop bot...\n')
    time.sleep(time_interval)

   
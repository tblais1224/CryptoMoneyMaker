from app.lib.common.exchange_api import Api
# import graphing
from app.lib.indicators.moving_average import MovingAverage
from app.lib.strategies.multi_ema import MultiEma
from app.data.markets import MARKETS
from app.lib.common.mysql import Db
import sys
import time
import signal
sys.path.append('/home/tom/Documents/CodingProjects/CryptoBot')

time_interval = 5

loop_count = 0
run = True

db = Db('crypto_bot')


def signal_handler(signal, frame):
    global run
    print('\nSTOPPING BOT')
    run = False


signal.signal(signal.SIGINT, signal_handler)

# using tether USDT
buying_power_coin = 'USDT'
# api call to get coin amount
buying_power_amount = 1000.00

# TODO: call binance and check wallet, set values for all coins
db.prep_db(buying_power_amount, buying_power_coin)


while run:
    loop_count += 1
    all_market_data = Api().get_market_price()
    for market in all_market_data:
        symbol = market['symbol']
        if MARKETS.get(symbol) != None and MARKETS[symbol]['trade'] == True:
            bid = float(market['bidPrice'])
            ask = float(market['askPrice'])
            bid_ask_avg = (bid+ask)/2
            MARKETS[symbol]['last_price'] = bid_ask_avg

            db.add_price(symbol, bid_ask_avg, bid, ask)
            print(
                f'market: {symbol}, bid ask avg: {bid_ask_avg}, bid: {bid}, ask: {ask}')
            
            sma = MovingAverage(symbol, MARKETS[symbol], 8).sma()
            prev_ema = MARKETS[symbol]['indicator']['ema_8']
            MARKETS[symbol]['indicator']['ema_8'] = MovingAverage(symbol, MARKETS[symbol], 8).ema()
            ema = MARKETS[symbol]['indicator']['ema_8']
            print(f'sma: {sma}, ema_8: {ema}, prev_ema_8: {prev_ema}\n')
            

            # # the safer option is probably to call the api for wallet amounts
            # coin_in_wallet = MARKETS[symbol]['holding_amount']
            # strategy_check = multi_ema(symbol, bid_ask_avg).buy_or_sell()

            # if buy_check(strategy_check, coin_in_wallet):
            #     # allocate % of buying power to trade, min trade size ten dollars
            #     # testing with trading 95% wallet of to btc
            #     purchasing_coin_amount = 0.95 * buying_power_amount / bid_ask_avg
            #     # make trade to api call
            #     # somehow confirm trade went through
            #     db.make_order('buy', bid_ask_avg, symbol, purchasing_coin_amount)

            # elif sell_check(strategy_check, coin_in_wallet):
            #     # sell all coin in wallet
            #     db.make_order('sell', bid_ask_avg, symbol, coin_in_wallet)

    print(
        f'Bot run count: {loop_count} done, continuing in {time_interval} seconds...')
    print('Press CTRL+c to sell off all coins and stop bot...\n')
    time.sleep(time_interval)


def buy_check(strategy_check, coin_in_wallet):
    return strategy_check == 'buy' and coin_in_wallet == 0.0 and buying_power_amount * 0.95 >= 10.0


def sell_check(strategy_check, coin_in_wallet):
    return strategy_check == 'sell' and coin_in_wallet > 0.0

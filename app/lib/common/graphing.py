import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


class live_chart(object):
    def __init__(self, market):
        self.market = market

    



style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)




# print(moving_average_test(btc_close_prices, 55))

# print('btc hist sma')
# print(MovingAverage(btc_close_prices).sma(55))

# plt.plot(btc_date, btc_close_prices, MovingAverage(btc_close_prices).sma(55))


# sma_8 = btc_close_prices.rolling(window=8).mean()
# sma_13 = btc_close_prices.rolling(window=13).mean()
# sma_21 = btc_close_prices.rolling(window=21).mean()
# sma_55 = btc_close_prices.rolling(window=55).mean()

# plt.plot(btc_date, sma_8, label='AMD 8 MIN SMA', color='orange')
# plt.plot(btc_date, sma_13, label='AMD 13 MIN SMA', color='magenta')
# plt.plot(btc_date, sma_21, label='AMD 13 MIN SMA', color='magenta')
# # plt.plot(btc_date, sma_55, label='AMD 13 MIN SMA', color='magenta')

# # plt.legend(loc='upper left')
# plt.show()

# plt.show()


# with open('btc_data.json') as f:
#     btc_data = json.load(f)

# btc_close_prices = []
# btc_date = []

# for interval in btc_data['result'][:1000]:
#     btc_close_prices.append(interval['C'])
#     btc_date.append(btc_data['result'].index(interval))


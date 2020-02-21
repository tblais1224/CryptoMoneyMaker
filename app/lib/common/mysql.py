import mysql.connector
from config.config_info import DB


class ConnectDb(object):
    def __init__(self, market, strategy='unspecified'):
        self.market = market
        self.strategy = strategy
        self.client = mysql.connector.connect(
            host=DB['host'],
            user=DB['user'],
            passwd=DB['password']
        )

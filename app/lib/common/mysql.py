import mysql.connector
from datetime import datetime
from config.config_info import DB


class Db(object):
    def __init__(self, database_name='crypto_bot'):
        self.mysqldb = mysql.connector.connect(
            host=DB['host'],
            user=DB['user'],
            password=DB['password'],
            database=database_name
        )
        self.client = self.mysqldb.cursor()


    def add_price(self, market, price, bid, ask):
        query = "INSERT INTO price (price, market, bid, ask) VALUES (%s, %s, %s, %s);"
        args = (price, market, bid, ask)
        self.client.execute(query, args)
        if self.client.lastrowid:
            print('last insert id', self.client.lastrowid)
            self.mysqldb.commit()
            return 1
        else:
            print('last insert id not found')
            return 0
        
    def make_order(self, order_type, price, market, amount, strategy=None):
        traded_currencies = market.split('-')
        if order_type == 'buy':
            self.update_coin_amount(amount, traded_currencies[0])
            self.update_coin_amount(0 - amount, traded_currencies[1])
        else:
            self.update_coin_amount(amount, traded_currencies[1])
            self.update_coin_amount(0 - amount, traded_currencies[0])
        self.client(
            f'INSERT INTO order_history (type, price, market, amount, strategy) VALUES ({order_type}, {price}, "{market}", {amount}, {strategy});')

    def get_price_history(self, market, range=1, from_date=None, to_date=datetime.now()):
        if from_date:
            return self.client.execute(f"SELECT price, bid, ask, market, date FROM price WHERE market = '{market}' AND date >= {from_date} AND date <= {to_date} ORDER BY date DESC;")
        return self.client.execute(f"SELECT price, bid, ask, market, date FROM price WHERE market = '{market}' ORDER BY date DESC LIMIT {range};")

    def get_coin_amount(self, type):
        return self.client(f'SELECT amount FROM wallet WHERE type = {type} AND date = MAX(date);')

    def get_wallet(self):
        return self.client(f'SELECT amount, type, date FROM wallet WHERE date IN (SELECT MAX(date) FROM wallet GROUP BY type)')

    def update_coin_amount(self, total_change, type):
        new_ammount = self.get_coin_amount(type) + total_change
        self.client(
            f'INSERT INTO wallet (amount, type) VALUES ({new_ammount}, {type});')
        return new_ammount

import mysql.connector
from datetime import datetime
from config.config_info import DB
from decimal import Decimal
from app.data.markets import MARKETS


TABLES = ['wallet', 'price', 'indicator', 'order_history']


class Db(object):
    def __init__(self, database_name='crypto_bot'):
        # self.__prepare_db()
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

    def make_order(self, order_type, price, market, amount, purchase_coin='USDT', strategy='Multi EMA'):
        coin_purchased = market.replace(purchase_coin, '')
        query = (
            'INSERT INTO order_history (type, price, market, amount, strategy) VALUES (%s, %s, %s, %s, %s);')
        args = (order_type, price, market, amount, strategy)
        self.client.execute(query, args)
        transaction_id = self.client.lastrowid
        if transaction_id:
            print('Transaction saved')
            self.mysqldb.commit()
        else:
            print('Transaction failed')
            return 0
        if order_type == 'buy':
            self.update_wallet(amount, coin_purchased, transaction_id)
            self.update_wallet(0 - amount * price,
                               purchase_coin, transaction_id)
        else:
            self.update_wallet(amount * price, purchase_coin, transaction_id)
            self.update_wallet(0 - amount, coin_purchased, transaction_id)

    def get_price_history(self, market, range=1, from_date=None, to_date=datetime.now()):
        if from_date:
            return self.client.execute(f"SELECT price, bid, ask, market, date FROM price WHERE market = '{market}' AND date >= {from_date} AND date <= {to_date} ORDER BY date DESC;")
        return self.client.execute(f"SELECT price, bid, ask, market, date FROM price WHERE market = '{market}' ORDER BY date DESC LIMIT {range};")

    def get_coin_amount(self, coin):
        query = (
            f'SELECT amount FROM wallet WHERE coin = "{coin}" ORDER BY date DESC LIMIT 1;')
        self.client.execute(query)
        result = self.client.fetchone()
        if result:
            print('Wallet lookup successful')
            self.mysqldb.commit()
            return result
        else:
            print('Wallet amount lookup failed')
            return 0

    def get_wallet(self):
        query = (
            'SELECT amount, coin, date FROM wallet WHERE date IN (SELECT MAX(date) FROM wallet GROUP BY coin)')
        self.client.execute(query)
        result = self.client.fetchall()
        if result:
            for coin_data in result:
                print(
                    f'Holding: {coin_data[0]} of {coin_data[1]}, as of {coin_data[2]}.')
            self.mysqldb.commit()
            return result
        else:
            print('Wallet lookup failed')
            return 0

    def update_wallet(self, total_change, coin, transaction_id):
        new_ammount = Decimal(self.get_coin_amount(coin)[
                              0]) + Decimal(total_change)
        query = (
            'INSERT INTO wallet (amount, coin, transaction_id) VALUES (%s, %s, %s);')
        args = (new_ammount, coin, transaction_id)
        self.client.execute(query, args)
        if self.client.lastrowid:
            print(f'Updated wallet amount: {coin} = {new_ammount}')
            self.mysqldb.commit()
            return new_ammount
        else:
            print('wallet update failed')
            return 0

    def clear_table(self, table):
        query = (f'TRUNCATE {table};')
        self.client.execute(query)
        if self.client.lastrowid:
            print(f'Removed all data from {table}')
            self.mysqldb.commit()
            return 1
        else:
            print('Failed to clear table')
            return 0

    def prep_db(self, buying_power, purchase_coin='USDT'):
        for table in TABLES:
            self.clear_table(table)
        query = (
            'INSERT INTO wallet (amount, coin, transaction_id) VALUES (%s, %s, %s);')
        for market in MARKETS:
            args = (0.0, market.replace(purchase_coin, ''), None)
            self.client.execute(query, args)
        args = (buying_power, purchase_coin, None)
        self.client.execute(query, args)
        if self.client.lastrowid:
            print(f'Database ready...')
            self.get_wallet()
            print('=================================================\n')
            self.mysqldb.commit()
            return 1
        else:
            print('Failed prep db')
            return 0

    #     query = ('DROP DATABASE IF EXISTS database_name;')
    #     self.client.execute(query)
    #     self.mysqldb.commit()
    #     self.client.close()
    #     self.
    #     query = ('SOURCE /home/tom/Documents/CodingProjects/CryptoBot/app/data/crypto_bot_db_backup.sql;')
    #     self.client.execute(query)
    #     self.mysqldb.commit()

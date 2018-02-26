
from binance.client import Client
from authentication import config
from cryptoMath import percentageChange
from kline import config as kLineConfig
from pprint import pprint
from copy import copy
from binance.helpers import date_to_milliseconds
from datetime import datetime
from Account import Account
from time import sleep
api_key = config["api_key"]
api_secret = config["api_secret"]

client = Client(api_key, api_secret)

def timestampToDatetime( timeStamp ):
    return str(datetime.fromtimestamp( timeStamp/ 1e3))

account = Account(balance=100)

ticker = "NEOBTC"

origin_jump = 4
second_jump = 2
drop = 1


def trading_algo(origin_jump, second_jump, drop, quantity, previous_price, new_price):
    if account.position_exists(ticker):
        pChange = percentageChange(account.get_positions[ticker]["value"]["price"], new_price)
        if pChange > second_jump:
            account.sell(float(new_price), quantity, ticker)
            order = client.create_order(
                symbol=ticker,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=.1)
        elif pChange < -drop:
            account.sell(float(new_price), quantity, ticker)
            order = client.create_order(
                symbol=ticker,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=.1)
    else:
        pChange = percentageChange(previous_price, new_price)
        if pChange > origin_jump: #
            account.buy( float(new_price), quantity, ticker)
            order = client.create_order(
                symbol=ticker,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=.1)
    log = "%s SYMBOL: %s Percentage Change: %s %s" % (str(datetime.now()), ticker, pChange, new_price)
    print log
    return account.get_balance()


def main():
    previous_price = None
    while(True):
        prices = client.get_all_tickers()
        neo_data = [x for x in prices if x['symbol'] == ticker][0]
        neo_price = float(neo_data['price'])
        if previous_price:
            print trading_algo(origin_jump, second_jump, drop, .1, previous_price, neo_price)
        previous_price = neo_price
        pprint(account.get_positions)
        sleep(3600)


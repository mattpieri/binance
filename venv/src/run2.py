import sys
from binance.client import Client
from authentication import config
from cryptoMath import percentageChange
from kline import config as kLineConfig
from pprint import pprint, pformat
from copy import copy
from binance.helpers import date_to_milliseconds
from datetime import datetime
from Account import Account
from time import sleep



def timestampToDatetime( timeStamp ):
    return str(datetime.fromtimestamp( timeStamp/ 1e3))

account = Account(balance=100)

ticker = "NEOBTC"

origin_jump =  .5
second_jump = .25
drop = .25


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
    logging.info(log)
    print log
    return account.get_balance()

import logging
logging.basicConfig(filename='/var/log/example2.log',level=logging.DEBUG,format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")



def main():
    logging.info( "\n\n%%%%%%%%%%%%%%%%% Starting Trader %%%%%%%%%%%%%%5 \n\n" )
    api_key = config["api_key"]
    api_secret = config["api_secret"]
   
    client = Client(api_key, api_secret)
   
    previous_price = None
    ticker = "NEOBTC"
   
    while(True):
    	prices = client.get_all_tickers()
    	neo_data = [x for x in prices if x['symbol'] == 'NEOBTC'][0]
    	neo_price = float(neo_data['price'])
        if previous_price:
            print trading_algo(origin_jump, second_jump, drop, .05, previous_price, neo_price)
        previous_price = neo_price
        logging.info(pformat(account.get_positions))
	logging.info("Sleeeping ...")
        sleep(120)

try:
	main()

except Exception as e:
	print e
	logging.info( "\n\n %%%%%%% ERROR %%%%%%%%  \n\n" + e )

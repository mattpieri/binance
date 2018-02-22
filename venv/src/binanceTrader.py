
from binance.client import Client
from authentication import config
from cryptoMath import percentageChange
from kline import config as kLineConfig
from pprint import pprint
from copy import copy
from binance.helpers import date_to_milliseconds
from datetime import datetime
from Account import Account
api_key = config["api_key"]
api_secret = config["api_secret"]

client = Client(api_key, api_secret)

def timestampToDatetime( timeStamp ):
    return str(datetime.fromtimestamp( timeStamp/ 1e3))

account = Account(balance=100)

ticker = "NEOUSDT"

# params = {
#     "origin_jump":[]
#     "secod_jump"
#     "drop"
#     "quantity"
# }

klines = client.get_historical_klines(ticker, "1h", "100 day ago UTC")
klines = [dict(zip(kLineConfig["columnNames"], x)) for x in klines]


def trading_algo(origin_jump, second_jump, drop, quantity):
    for i in range(0, len(klines) - 1):
        if account.position_exists(ticker):
            pChange = percentageChange(account.get_positions[ticker]["value"]["price"], klines[i + 1]["Close"])
            if pChange > second_jump:
                account.sell(float(klines[i]["Close"]), quantity, ticker)
            elif pChange < -drop:
                account.sell(float(klines[i]["Close"]), quantity, ticker)
        else:
            pChange = percentageChange(klines[i]["Close"], klines[i + 1]["Close"])
            if pChange > origin_jump: #
                account.buy( float(klines[i]["Close"]), quantity, ticker)
        #log = "%s SYMBOL: %s Percentage Change: %s %s" % (timestampToDatetime(klines[i]["Close time"]), ticker, pChange, klines[i + 1]["Close"])
        #print log
    return account.get_balance()

result = dict()
for origin_jump in range(1, 5):
    for second_jump in range(1, 5):
        drop = 2
        result[str(trading_algo(origin_jump, second_jump, drop, .5))] = "%d %d %d %d" % (origin_jump, second_jump, drop, .5)

for key in sorted(result.iterkeys()):
    print key + " " + result[key]

#pprint(account.get_positions)
#pprint(account.get_balance())


#place a test market buy order, to place an actual order use the create_order function
order = client.create_test_order(
    symbol='ICXETH',
    side=Client.SIDE_SELL,
    type=Client.ORDER_TYPE_MARKET,
    quantity=2)

#
# # get market depth
# depth = client.get_order_book(symbol='BNBBTC')
#
# # place a test market buy order, to place an actual order use the create_order function
# order = client.create_test_order(
#     symbol='BNBBTC',
#     side=Client.SIDE_BUY,
#     type=Client.ORDER_TYPE_MARKET,
#     quantity=100)
#
# # get all symbol prices
# prices = client.get_all_tickers()
#
# # withdraw 100 ETH
# # check docs for assumptions around withdrawals
# from binance.exceptions import BinanceAPIException, BinanceWithdrawException
# try:
#     result = client.withdraw(
#         asset='ETH',
#         address='<eth_address>',
#         amount=100)
# except BinanceAPIException as e:
#     print(e)
# except BinanceWithdrawException as e:
#     print(e)
# else:
#     print("Success")
#
# # fetch list of withdrawals
# withdraws = client.get_withdraw_history()
#
# # fetch list of ETH withdrawals
# eth_withdraws = client.get_withdraw_history(asset='ETH')
#
# # get a deposit address for BTC
# address = client.get_deposit_address(asset='BTC')
#
# # start aggregated trade websocket for BNBBTC
# def process_message(msg):
#     print("message type: {}".format(msg['e']))
#     print(msg)
#     # do something
#
# from binance.websockets import BinanceSocketManager
# bm = BinanceSocketManager(client)
# bm.start_aggtrade_socket('BNBBTC', process_message)
# bm.start()
#
# # get historical kline data from any date range
#
# # fetch 1 minute klines for the last day up until now
# klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
#
# # fetch 30 minute klines for the last month of 2017
# klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")
#
# # fetch weekly klines since it listed
# klines = client.get_historical_klines("NEOBTC", KLINE_INTERVAL_1WEEK, "1 Jan, 2017")
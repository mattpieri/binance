from datetime import datetime
from pprint import pprint

class Account(object):
    def __init__(self, balance=0):
        self.orig_cash_balance = balance
        self.trades = []
        self.positions = dict()

    def buy(self, price, qauntity, ticker):
        if not self.positions.get(ticker):
            self.positions[ticker] = {"transactions": {
                datetime.now(): {"type": "BUY", "ticker": ticker, "price": price, "quantity": qauntity}}}
        else:
            transactions = self.positions[ticker]["transactions"]
            transactions[datetime.now()] = {"type": "BUY", "ticker": ticker, "price": price, "quantity": qauntity}
            self.positions[ticker]["transactions"] = transactions
        self.recalucate_position(ticker)

    def sell(self, price, qauntity, ticker):
        if not self.positions.get(ticker):
            self.positions[ticker] = {"transactions": {
                datetime.now(): {"type": "SELL", "ticker": ticker, "price": price, "quantity": qauntity}}}
        else:
            transactions = self.positions[ticker]["transactions"]
            transactions[datetime.now()] = {"type": "SELL", "ticker": ticker, "price": price, "quantity": qauntity}
            self.positions[ticker]["transactions"] = transactions
        self.recalucate_position(ticker)

    def recalucate_position(self, ticker):
        position = self.positions.get(ticker)
        if not position:
            raise Exception("Why are you recaluclating on poistion with no trades?")

        quantity = 0
        cash = 0
        for key in sorted(position["transactions"].iterkeys()):
            if position["transactions"][key]["type"] == "BUY":
                cash -= position["transactions"][key]["price"] * position["transactions"][key]["quantity"]
                quantity += position["transactions"][key]["quantity"]
            elif position["transactions"][key]["type"] == "SELL":
                cash += position["transactions"][key]["price"] * position["transactions"][key]["quantity"]
                quantity -= position["transactions"][key]["quantity"]
            else:
                raise Exception("You fucked something up ")

        last_transcation = sorted(position["transactions"].iterkeys())[0]
        price = position["transactions"][last_transcation]["price"]

        if quantity == 0:
            position["value"] = {}
        else:
            position["value"] = {"price": price, "quantity": quantity}

        position["cash"] = cash

        self.positions[ticker] = position


    @property
    def get_trades(self):
        return self.trades

    @property
    def get_positions(self):
        return self.positions

    def get_position(self, ticker):
        return self.positions.get(ticker)

    #def __str__(self):
    #    pprint(self.positions)
    #    return ""

    def position_exists(self, ticker):
        if ticker not in self.positions.keys():
            return False
        if self.positions[ticker].get("value") and self.positions[ticker]["value"] != {}:
            return True
        return False

    def get_balance(self):
        cash_balance = self.orig_cash_balance
        for ticker, position in self.positions.iteritems():
            if position.get("cash"):
                cash_balance += position["cash"]
        return cash_balance
import unittest
from Account import Account
from pprint import pprint

class MyTestCase(unittest.TestCase):

    def test_buy(self):
        ticker = "NEOUSDT"
        price = 100
        quantity = .5
        test_account = Account(balance=100)
        test_account.buy(price, quantity, ticker)

        result = test_account.position_exists("NEOUSDT")
        self.assertEqual(True, result)

        position = test_account.get_position("NEOUSDT")
        self.assertEqual(float(-50), position["cash"])

    def test_sell(self):
        ticker = "NEOUSDT"
        price = 100
        quantity = .5
        test_account = Account(balance=100)
        test_account.sell(price, quantity, ticker)

        result = test_account.position_exists("NEOUSDT")
        self.assertEqual(True, result)


    def test_buy_sell(self):
        ticker = "NEOUSDT"
        price = 1000
        quantity = 1
        test_account = Account(balance=100)
        test_account.buy(price, quantity, ticker)
        str(test_account)

        price = 1005
        quantity = 1
        test_account.sell(price, quantity, ticker)
        str(test_account)
        result = test_account.position_exists("NEOUSDT")
        self.assertEqual(False, result)

    def test_buy_sell_2(self):
        ticker = "NEOUSDT"
        price = 100
        quantity = .5
        test_account = Account(balance=100)
        test_account.buy(price, quantity, ticker)
        self.assertEqual(test_account.get_balance(), 50)
        self.assertEqual(test_account.position_exists(ticker), True)
        test_account.buy(price, quantity, ticker)
        self.assertEqual(test_account.get_balance(), 0)
        test_account.sell(100, 1, ticker)
        self.assertEqual(test_account.get_balance(), 100)
        self.assertEqual(test_account.position_exists(ticker), False)
        str(test_account)

if __name__ == '__main__':
    unittest.main()

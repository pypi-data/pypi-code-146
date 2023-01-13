# Importing external libraries
import sys
import unittest

# Importing libraries we want to test
sys.path.append('../')
import src.goquant.goquant as gq



class TestInitialization(unittest.TestCase):

    def setUp(self):
        self.gq = gq.GoQuant()

    def test_binance(self):
        self.assertTrue(self.gq.binance)

    def test_huobi(self):
        self.assertTrue(self.gq.huobi)

    def test_okex(self):
        self.assertTrue(self.gq.okex)

    def test_coinbase(self):
        self.assertTrue(self.gq.coinbase)

    def test_bybit(self):
        self.assertTrue(self.gq.bybit)

    def test_deribit(self):
        self.assertTrue(self.gq.deribit)

    def test_bitfinex(self):
        self.assertTrue(self.gq.bitfinex)

    def test_bitstamp(self):
        self.assertTrue(self.gq.bitstamp)



if __name__ == "__main__":
    unittest.main()
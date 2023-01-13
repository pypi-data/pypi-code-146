# Importing external libraries
import sys
import unittest

# Importing libraries we want to test
sys.path.append('../')
import src.goquant.goquant as gq

class TestBinanceStatic(unittest.TestCase):

    def setUp(self):
        self.gq = gq.GoQuant()

    def test_huobi_static_ohlcv(self):
        res = self.gq.huobi.spot.ohlcv('BTCUSDT')
        self.assertTrue(res)

    def test_huobi_static_orderbook(self):
        res = self.gq.huobi.spot.orderbook('BTCUSDT')
        self.assertTrue(res)

    def test_huobi_static_quote(self):
        res = self.gq.huobi.spot.quote('BTCUSDT')
        self.assertTrue(res)

    def test_huobi_static_trades(self):
        res = self.gq.huobi.spot.trades('BTCUSDT', 1)
        self.assertTrue(res)



if __name__ == "__main__":
    unittest.main()
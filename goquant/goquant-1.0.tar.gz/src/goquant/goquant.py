# Importing external libraries
import os
from os import environ

# Importing internal libraries
from .exchanges.binance.binance import Binance
from .exchanges.huobi.huobi import Huobi
from .exchanges.okex.okex import Okex
from .exchanges.coinbase.coinbase import Coinbase
from .exchanges.bybit.bybit import Bybit
from .exchanges.deribit.deribit import Deribit
from .exchanges.bitfinex.bitfinex import Bitfinex
from .exchanges.bitstamp.bitstamp import Bitstamp



class GoQuant():

    def __init__(self):

        self.tenant_live_url = 'wss://api2.goquant.io/'
        self.tenant_historical_url = 'https://api2.goquant.io/'

        # For localhost testing
        # self.tenant_live_url = 'ws://localhost:8082/'
        # self.tenant_historical_url = 'http://localhost:8082/'

        self.binance = Binance(self.tenant_live_url, self.tenant_historical_url)
        self.huobi = Huobi(self.tenant_live_url, self.tenant_historical_url)        
        self.okex = Okex(self.tenant_live_url, self.tenant_historical_url)        
        self.coinbase = Coinbase(self.tenant_live_url, self.tenant_historical_url)        
        self.bybit = Bybit(self.tenant_live_url, self.tenant_historical_url)        
        self.deribit = Deribit(self.tenant_live_url, self.tenant_historical_url)        
        self.bitfinex = Bitfinex(self.tenant_live_url, self.tenant_historical_url)        
        self.bitstamp = Bitstamp(self.tenant_live_url, self.tenant_historical_url)
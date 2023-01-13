import requests
from websocket import create_connection


class HuobiSpot():

    def __init__(self, static_url, live_url):
        self.static_url = static_url 
        self.live_url = live_url

    def ohlcv(self, symbol):
        return requests.get(f'{self.static_url}api/static/huobi/spot?data_type=ohlcv&symbol={symbol.lower()}').json()

    def orderbook(self, symbol):
        return requests.get(f'{self.static_url}api/static/huobi/spot?data_type=orderbook_l2&symbol={symbol.lower()}').json()

    def quote(self, symbol):
        return requests.get(f'{self.static_url}api/static/huobi/spot?data_type=quote&symbol={symbol.lower()}').json()

    def trades(self, symbol, limit):
        return requests.get(f'{self.static_url}api/static/huobi/spot?data_type=trades&symbol={symbol.lower()}&limit={limit}').json()

    def live_data(self, symbol, data_type):
        ws = create_connection(f'{self.live_url}?symbol={symbol.lower()}&data_type={data_type}')
        while True: 
            print(symbol, ws.recv())
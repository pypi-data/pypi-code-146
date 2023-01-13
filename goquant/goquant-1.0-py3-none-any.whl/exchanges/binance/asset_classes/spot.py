import requests
from websocket import create_connection


class BinanceSpot():

    def __init__(self, live_url, static_url):
        self.live_url = live_url
        self.static_url = static_url

    def ohlcv(self, symbol):
        return requests.get(f'{self.static_url}api/static/binance/spot?data_type=ohlcv&symbol={symbol.upper()}').json()

    def orderbook(self, symbol):
        return requests.get(f'{self.static_url}api/static/binance/spot?data_type=orderbook_l2&symbol={symbol.upper()}').json()

    def quote(self, symbol):
        return requests.get(f'{self.static_url}api/static/binance/spot?data_type=quote&symbol={symbol.upper()}').json()

    def trades(self, symbol, limit):
        return requests.get(f'{self.static_url}api/static/binance/spot?data_type=trades&symbol={symbol.upper()}&limit={limit}').json()

    # Getting live websocket data
    def live_data(self, symbol, data_type):
        ws = create_connection(f"{self.live_url}api/live/binance/spot?symbol={symbol}&data_type={data_type}")
        # TODO: Add subscribe message
        while True:
            try: 
                print(symbol, ws.recv())
            except KeyboardInterrupt:
                # TODO: Push unsubscribe to websocket API
                ws.close()
                return





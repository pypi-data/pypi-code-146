import requests
from websocket import create_connection


class OkexSpot():

    def __init__(self, live_url, historical_url):
        self.live_url = live_url
        self.historical_url = historical_url

    def live_data(self, symbol, data_type):

        ws = create_connection(f"{self.live_url}api/live/okex/spot?symbol={symbol.lower()}&data_type={data_type}")
        while True: 
            print(symbol, ws.recv())






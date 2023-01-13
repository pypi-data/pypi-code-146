import requests
from websocket import create_connection


class BitstampSpot():

    def __init__(self, live_url, static_url):
        self.live_url = live_url
        self.static_url = static_url

    def live_data(self, symbol, data_type):
        ws = create_connection(f"{self.live_url}api/live/bitstamp/spot?symbol={symbol.upper()}&data_type={data_type}")
        while True: 
            print(symbol, ws.recv())






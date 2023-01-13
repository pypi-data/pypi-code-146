from .asset_classes.spot import CoinbaseSpot


class Coinbase():

    def __init__(self, live_url, historical_url):

        self.live_url = live_url
        self.historical_url = historical_url

        self.spot = CoinbaseSpot(self.live_url, self.historical_url)

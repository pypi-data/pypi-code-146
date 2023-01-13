from .asset_classes.spot import BitfinexSpot


class Bitfinex():

    def __init__(self, live_url, historical_url):

        self.live_url = live_url
        self.historical_url = historical_url

        self.spot = BitfinexSpot(self.live_url, self.historical_url)

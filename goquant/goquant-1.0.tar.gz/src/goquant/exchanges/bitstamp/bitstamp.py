from .asset_classes.spot import BitstampSpot


class Bitstamp():

    def __init__(self, live_url, historical_url):

        self.live_url = live_url
        self.historical_url = historical_url

        self.spot = BitstampSpot(self.live_url, self.historical_url)

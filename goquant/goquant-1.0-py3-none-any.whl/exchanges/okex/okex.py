from .asset_classes.spot import OkexSpot


class Okex():

    def __init__(self, live_url, historical_url):

        self.live_url = live_url
        self.historical_url = historical_url

        self.spot = OkexSpot(self.live_url, self.historical_url)

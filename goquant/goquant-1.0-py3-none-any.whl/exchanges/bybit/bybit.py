from .asset_classes.spot import BybitSpot


class Bybit():

    def __init__(self, live_url, historical_url):

        self.live_url = live_url
        self.historical_url = historical_url

        self.spot = BybitSpot(self.live_url, self.historical_url)

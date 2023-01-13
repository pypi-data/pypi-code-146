from .asset_classes.spot import DeribitSpot


class Deribit():

    def __init__(self, live_url, historical_url):

        self.live_url = live_url
        self.historical_url = historical_url

        self.spot = DeribitSpot(self.live_url, self.historical_url)

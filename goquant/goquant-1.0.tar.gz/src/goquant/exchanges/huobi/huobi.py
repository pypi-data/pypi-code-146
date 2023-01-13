from .asset_classes.spot import HuobiSpot


class Huobi():

    def __init__(self, live_url, historical_url):

        self.live_url = live_url
        self.historical_url = historical_url
        
        self.spot = HuobiSpot('http://localhost:8082/api/static/huobi/spot', 'ws://localhost:8082/api/live/huobi/spot')

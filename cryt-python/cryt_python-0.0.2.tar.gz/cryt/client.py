import time

import requests

from cryt.base import BaseClient


class Client(BaseClient):
    def __init__(self, base_url=None, public_key=None, private_key=None):
        super().__init__(base_url, public_key=public_key, private_key=private_key)
        self.session = self._init_session()

    def _init_session(self):
        headers = self._get_headers()
        session = requests.session()
        session.headers.update(headers)
        return session

    def _request(self, method, uri, **kwargs):
        response = self.session.request(method, uri, **kwargs)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response):
        try:
            return response.json()
        except:
            return response

    def _request_api(self, method, path, **kwargs):
        uri = self._create_api_uri(path)
        return self._request(method, uri, **kwargs)

    def close_connection(self):
        if self.session:
            self.session.close()

    # API

    def sign_up(self, data):
        return self._request_api("POST", "api/SignUp", json=data)

    # MarketAPI

    def get_market_summary(self, pair):
        path = "market/get-market-summary"
        path = f"{path}/{pair}" if pair else path
        return self._request_api("GET", path)

    def get_trade_history(self, pair):
        path = f"market/get-trade-history/{pair}"
        return self._request_api("GET", path)

    def get_bid_ask_price(self, pair):
        path = f"market/get-bid_ask-price/{pair}"
        return self._request_api("GET", path)

    def get_open_orders(self, pair, side, depth):
        path = f"market/get-open-orders/{pair}/{side}/{depth}"
        return self._request_api("GET", path)

    def get_currency_price(self, pair):
        path = f"market/get-currency-price/{pair}"
        return self._request_api("GET", path)

    def get_currency_usd_rate(self, currency):
        path = "market/get-currency-usd-rate"
        path = f"{path}/{currency}" if currency else path
        return self._request_api("GET", path)

    def depth(self, pair, limit):
        path = "market/depth"
        params = {
            "symbol": pair,
            "limit": limit,
        }
        return self._request_api("GET", path, params=params)

    def get_chart_data(self, base_currency, quote_currency, interval, limit):
        path = "market/get-chart-data"
        params = {
            "baseCurrency": base_currency,
            "quoteCurrency": quote_currency,
            "interval": interval,
            "limit": limit,
            "timestamp": int(time.time() * 1000),
        }
        return self._request_api("GET", path, params=params)

    # OrderAPI

    def place_order(self, data):
        path = "order/v2/PlaceOrder"
        return self._request_api("POST", path, json=data)

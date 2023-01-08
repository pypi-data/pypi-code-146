import base64
import hmac
import json
import requests
import urllib
import urllib.request
from urllib.parse import urljoin
from time import time
from ccxt import Exchange as CcxtBaseExchange
from ccxt.base.decimal_to_precision import decimal_to_precision, TRUNCATE
from ccxtools.exchange import Exchange
from ccxtools.tools import add_query_to_url


class Bingx(Exchange):
    BASE_URL = 'https://api-swap-rest.bingbon.pro/api/v1'

    def __init__(self, who, market, config):
        super().__init__(market)
        self.API_KEY = config(f'BINGX_API_KEY{who}')
        self.SECRET_KEY = config(f'BINGX_SECRET_KEY{who}')
        self.contract_sizes = self.get_contract_sizes()

        self.ccxt_exchange = CcxtBaseExchange()

    def request_get(self, url):
        for i in range(10):
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()

    def request_post(self, url, params):
        for i in range(10):
            params['timestamp'] = int(time() * 1000)

            params_str = '&'.join([f'{x}={params[x]}' for x in sorted(params)])

            signature_msg = f'POST/api/v1{url}{params_str}'
            signature = hmac.new(self.SECRET_KEY.encode('utf-8'), signature_msg.encode('utf-8'), 'sha256').digest()

            params_str += '&sign=' + urllib.parse.quote(base64.b64encode(signature))

            request = urllib.request.Request(Bingx.BASE_URL + url, params_str.encode('utf-8'),
                                             {'User-Agent': 'Mozilla/5.0'})
            post = urllib.request.urlopen(request).read()

            json_response = json.loads(post.decode('utf-8'))

            if 'invalid timestamp' not in json_response['msg']:
                return json_response
            from pprint import pprint
            pprint(json_response)

    def get_contract_sizes(self):
        """
        :return: {
            'BTC': 0.1,
            'ETH': 0.01,
            ...
        }
        """
        contracts = self.get_contracts()['data']['contracts']

        sizes = {}
        for contract in contracts:
            ticker = contract['asset']
            size = float(contract['size'])

            sizes[ticker] = size

        return sizes

    def get_balance(self, ticker):
        """
        :param ticker: <String> ticker name. ex) 'USDT', 'BTC'
        :return: <Int> balance amount
        """
        response = self.get_account_asset(ticker)
        return response['data']['account']['equity']

    def get_position(self, ticker: str) -> float:
        total = 0
        # long, short 양쪽 모두 position을 갖고 있는 경우가 있음
        for position in self.get_swap_positions()['data']['positions']:
            if position['symbol'] == f'{ticker}-USDT':
                absolute_amount = float(position['volume'])
                if position['positionSide'] == 'Long':
                    total += absolute_amount
                else:
                    total -= absolute_amount
        return total

    def post_market_order(self, ticker, side, open_close, amount):
        """
        :param ticker: <String>
        :param side: <Enum: "buy" | "sell">
        :param open_close: <Enum: "open" | "close">
        :param amount: <Float | Int>
        :return: <Float> average filled price
        """
        if side == 'buy':
            param_side = 'Bid'
        elif side == 'sell':
            param_side = 'Ask'

        res = self.post_order(ticker, param_side, amount, 'Market', open_close.capitalize())
        try:
            order_id = res['data']['orderId']
        except:
            raise Exception(res)
        order_info = self.get_order(ticker, order_id)['data']
        return order_info['avgFilledPrice']

    def get_precise_order_amount(self, ticker, ticker_amount):
        """
        :param ticker: <String>
        :param ticker_amount: <Float>
        :return: <Float>
        """
        contract_size = self.contract_sizes[ticker]
        precision = self.ccxt_exchange.precision_from_string(str(contract_size))

        return float(decimal_to_precision(ticker_amount, TRUNCATE, precision))

    def get_last_price(self, ticker: str) -> float:
        return float(self.get_latest_price(ticker)['data']['tradePrice'])

    """
    Market Interface
    """

    def get_contracts(self):
        """
        :return: {
            'code': <Int>,
            'data': {
                {
                    'contracts': [
                        {
                            'asset': 'BTC',
                            'contractId': '100',
                            'currency': 'USDT',
                            'feeRate': 0.0005,
                            'maxLongLeverage': 100,
                            'maxShortLeverage': 100,
                            'name': 'BTC',
                            'pricePrecision': 2,
                            'size': '0.0001',
                            'status': 1,
                            'symbol': 'BTC-USDT',
                            'tradeMinLimit': 1,
                            'volumePrecision': 4
                        },
                        {
                        },
                        ...
                    ]
                }
            },
            'msg': <String> ex) 'Success'
        }
        """
        url = Bingx.BASE_URL + '/market/getAllContracts'
        return self.request_get(url)

    def get_latest_price(self, ticker):
        """
        :param ticker:
        :return: {
            "code": 0,
            "msg": "",
            "data": {
              "tradePrice": "50000.18",
              "indexPrice": "50000.18",
              "fairPrice": "50000.18"
            }
        }
        """
        url = Bingx.BASE_URL + '/market/getLatestPrice'
        query = {'symbol': f'{ticker}-USDT'}
        return self.request_get(add_query_to_url(url, query))

    def get_market_depth(self, ticker):
        """
        :param ticker: <String>
        :return: {
            'asks': [
                {
                    'p': 19153.3274,
                    'v': 8.3473
                },
                {
                    'p': 19153.341,
                    'v': 3.3524
                },
                ...
            ],
            'bids': [
                {
                    'p': 19152.6914,
                    'v': 38.871
                },
                {
                    'p': 19152.4835,
                    'v': 2.7036
                },
                ...
            ],
            'ts': '1656868209523'
        }
        """
        url = Bingx.BASE_URL + '/market/getMarketDepth'
        query = {'symbol': f'{ticker}-USDT'}
        return self.request_get(add_query_to_url(url, query))['data']

    def get_ticker(self, ticker=''):
        """
        :return: {
            'code': <Int>,
            'data': {
                {
                    'tickers': [
                        {
                            "symbol": "BTC-USDT",
                            "priceChange": "10.00",
                            "priceChangePercent": "10",
                            "lastPrice": "5738.23",
                            "lastVolume": "31.21",
                            "highPrice": "5938.23",
                            "lowPrice": "5238.23",
                            "volume": "23211231.13",
                            "dayVolume": "213124412412.47",
                            "openPrice": "5828.32"
                        },
                        {
                        },
                        ...
                    ]
                }
            },
            'msg': <String>
        }
        """
        url = Bingx.BASE_URL + '/market/getTicker'
        query = {}
        if ticker:
            query['symbol'] = f'{ticker}-USDT'
        return self.request_get(add_query_to_url(url, query))

    """
    Account Interface
    """

    def get_account_asset(self, ticker):
        """
        :param ticker: <String> ticker name. ex) 'USDT', 'BTC'
        :return: {
            'code': 0,
            'data': {
                'account': {
                    'availableMargin': 4613.7489,
                    'balance': 11620.2463,
                    'currency': 'USDT',
                    'equity': 17196.776,
                    'freezedMargin': 0,
                    'longLeverage': 5,
                    'realisedPNL': 220.1801,
                    'shortLeverage': 5,
                    'unrealisedPNL': 5576.5298,
                    'usedMargin': 12583.0271,
                    'userId': '975609663951343623'
                }
            },
            'msg': '',
            'ttl': 1
        }
        """
        params = {
            'apiKey': self.API_KEY,
            'currency': ticker
        }
        return self.request_post('/user/getBalance', params)

    def get_swap_positions(self):
        params = {
            'symbol': '',
            'apiKey': self.API_KEY
        }
        return self.request_post('/user/getPositions', params)

    """
    Trade Interface
    """

    def post_order(self, ticker, side, amount, type, open_close):
        """
        :param ticker: <String>
        :param side: <Enum: "Bid" | "Ask">
        :param amount: <Float | Int>
        :param type: <Enum: "Market" | "Limit">
        :param open_close: <Enum: "Open" | "Close">
        :return: {
            'code': 0,
            'data': {
                'orderId': '1544719796619186176'
            },
            'msg': '',
            'ttl': 1
        }
        """
        symbol = f'{ticker}-USDT'
        precision = self.ccxt_exchange.precision_from_string(str(self.contract_sizes[ticker]))
        amount = decimal_to_precision(amount, TRUNCATE, precision)

        params = {
            'symbol': symbol,
            'apiKey': self.API_KEY,
            'side': side,
            'entrustPrice': 0,
            'entrustVolume': amount,
            'tradeType': type,
            'action': open_close
        }
        return self.request_post('/user/trade', params)

    def get_order(self, ticker, order_id):
        """
        :param ticker: <String>
        :param order_id: <String>
        :return: {
            'code': 0,
            'data': {
                'action': 'Open',
                'avgFilledPrice': 0.3232,
                'commission': -0.002585,
                'entrustPrice': 0.323,
                'entrustTm': '2022-07-06T16:15:28Z',
                'entrustVolume': 20,
                'filledVolume': 20,
                'orderId': '1544716667815202816',
                'profit': 0,
                'side': 'Bid',
                'status': 'Filled',
                'tradeType': 'Market',
                'updateTm': '2022-07-06T16:15:28Z'
            },
            'msg': '',
            'ttl': 1
        }
        """
        params = {
            'apiKey': self.API_KEY,
            'symbol': f'{ticker}-USDT',
            'orderId': order_id
        }
        return self.request_post('/user/queryOrderStatus', params)

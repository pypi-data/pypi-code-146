from decimal import Decimal
import ccxt
from ccxtools.exchange import CcxtExchange


class Bybit(CcxtExchange):

    def __init__(self, who, market, config):
        super().__init__(market)
        self.ccxt_inst = ccxt.bybit({
            'apiKey': config(f'BYBIT_API_KEY{who}'),
            'secret': config(f'BYBIT_SECRET_KEY{who}')
        })
        self.contract_sizes = self.get_contract_sizes()

    def get_contract_sizes(self):
        """
        :return: {
            'BTC': 0.1,
            'ETH': 0.01,
            ...
        }
        """
        if self.market == 'USDT':
            contracts = self.ccxt_inst.fetch_markets()

            sizes = {}
            for contract in contracts:
                if not contract['active'] or not contract['linear']:
                    continue

                ticker = contract['base']
                size = float(contract['info']['lot_size_filter']['qty_step'])

                sizes[ticker] = size

            return sizes

    def get_position(self, ticker: str) -> float:
        # long, short 양쪽 모두 position을 갖고 있는 경우가 있음
        positions = self.ccxt_inst.private_linear_get_position_list({'symbol': f'{ticker}USDT'})['result']
        return sum(-float(position['free_qty']) for position in positions)

    def post_market_order(self, ticker, side, open_close, amount):
        """
        :param ticker: <String>
        :param side: <Enum: "buy" | "sell">
        :param open_close: <Enum: "open" | "close">
        :param amount: <Float | Int>
        :return: <Float> average filled price
        """
        if self.market == 'USDT':
            symbol = f'{ticker}/USDT'
            if open_close == 'open':
                extra_params = {}
            elif open_close == 'close':
                extra_params = {'reduce_only': True}
            order_id = self.ccxt_inst.create_market_order(symbol, side, amount, params=extra_params)['id']

            trade_info = self.ccxt_inst.fetch_order(order_id, symbol)
            return trade_info['average']

    def get_max_trading_qtys(self):
        """
        :return: {
            'BTC': Decimal('100'),
            'ETH': Decimal('1000'),
            ...
        }
        """
        markets = self.ccxt_inst.fetch_markets()

        result = {}
        for market in markets:
            if not market['linear']:
                continue

            ticker = market['base']
            result[ticker] = Decimal(market['info']['lot_size_filter']['max_trading_qty'])

        return result

    def get_risk_limit(self, ticker):
        """
        :param ticker: <String> ticker name ex) 'BTC', 'USDT'
        :return: [
            {
                'created_at': '2022-06-23 15:04:07.187882',
                'id': '1',
                'is_lowest_risk': '1',
                'limit': '2000000',
                'maintain_margin': '0.005',
                'max_leverage': '100',
                'section': ['1', '3', '5', '10', '25', '50', '80'],
                'starting_margin': '0.01',
                'symbol': 'BTCUSDT',
                'updated_at': '2022-06-23 15:04:07.187884'
            },
            {
                'created_at': '2022-06-23 15:04:07.187884',
                'id': '2',
                'is_lowest_risk': '0',
                'limit': '4000000',
                'maintain_margin': '0.01',
                'max_leverage': '57.15',
                'section': ['1', '2', '3', '5', '10', '25', '50'],
                'starting_margin': '0.0175',
                'symbol': 'BTCUSDT',
                'updated_at': '2022-06-23 15:04:07.187885'},
            },
            ...
        ]
        """
        if self.market == 'USDT':
            return self.ccxt_inst.public_linear_get_risk_limit({
                'symbol': f'{ticker}USDT'
            })

    def set_risk_limit(self, ticker, side, risk_id):
        if self.market == 'USDT':
            try:
                return self.ccxt_inst.private_linear_post_position_set_risk({
                    'symbol': f'{ticker}USDT',
                    'side': side,
                    'risk_id': risk_id
                })
            except ccxt.errors.ExchangeError as exchange_error:
                if 'risk id not modified' in str(exchange_error):
                    return {
                        'ret_msg': 'OK',
                        'result': {
                            'risk_id': risk_id
                        }
                    }

                raise Exception(exchange_error)

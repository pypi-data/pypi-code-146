import ccxt
from ccxtools.exchange import CcxtExchange


class Ftx(CcxtExchange):

    def __init__(self, who, market, config):
        super().__init__(market)

        self.ccxt_inst = ccxt.ftx({
            'apiKey': config(f'FTX_API_KEY{who}'),
            'secret': config(f'FTX_SECRET_KEY{who}')
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
            contracts = self.ccxt_inst.publicGetFutures()['result']

            sizes = {}
            for contract in contracts:
                if not contract['perpetual'] or not contract['enabled']:
                    continue

                ticker = contract['underlying']
                size = float(contract['sizeIncrement'])

                sizes[ticker] = size

            return sizes

    def get_position(self, ticker: str) -> float:
        for position in self.ccxt_inst.fetch_positions():
            if position['symbol'] == f'{ticker}-PERP':
                return float(position['info']['netSize'])
        return 0

    def post_market_order(self, ticker, side, open_close, amount):
        """
        :param ticker: <String>
        :param side: <Enum: "buy" | "sell">
        :param open_close: <Enum: "open" | "close">
        :param amount: <Float | Int>
        :return: <Float> average filled price
        """
        if self.market == 'USDT':
            symbol = f'{ticker}-PERP'
            res = self.ccxt_inst.create_market_order(symbol, side, amount)

            for i in range(10):
                order_info = self.ccxt_inst.fetch_order(res['id'], symbol)
                if order_info['average']:
                    return order_info['average']

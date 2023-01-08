import ccxt
from ccxtools.exchange import CcxtExchange


class Okx(CcxtExchange):

    def __init__(self, who, market, config):
        super().__init__(market)
        self.ccxt_inst = ccxt.okex({
            'apiKey': config(f'OKX_API_KEY{who}'),
            'secret': config(f'OKX_SECRET_KEY{who}'),
            'password': config(f'OKX_PASSWORD{who}'),
        })

    def get_contract_sizes(self):
        """
        :return: {
            'BTC': 0.1,
            'ETH': 0.01,
            ...
        }
        """
        if self.market == 'USDT':
            contracts = self.ccxt_inst.publicGetPublicInstruments(params={'instType': 'SWAP'})['data']

            sizes = {}
            for contract in contracts:
                if contract['settleCcy'] != 'USDT' or contract['state'] != 'live':
                    continue

                ticker = contract['ctValCcy']
                size = float(contract['ctVal'])

                sizes[ticker] = size

            return sizes

    def post_market_order(self, ticker, side, open_close, amount):
        pass

    def set_leverage(self, ticker, leverage):
        if self.market == 'USDT':
            return self.ccxt_inst.set_leverage(leverage, f'{ticker}-USDT-SWAP', {'mgnMode': 'cross'})

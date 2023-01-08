import ccxt
from ccxtools.exchange import CcxtExchange


class Huobi(CcxtExchange):

    def __init__(self, who, market, config):
        super().__init__(market)

        if market == 'USDT':
            self.ccxt_inst = ccxt.huobi({
                'apiKey': config(f'HUOBI_API_KEY{who}'),
                'secret': config(f'HUOBI_SECRET_KEY{who}'),
                'options': {
                    'defaultType': 'swap',
                    'defaultSubType': 'linear'
                }
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
                if contract['info']['contract_status'] != '1':
                    continue

                ticker = contract['base']
                size = float(contract['info']['contract_size'])

                sizes[ticker] = size

            return sizes

    def get_balance(self, ticker):
        """
        :param ticker: <String> Ticker name. ex) 'USDT', 'BTC'
        :return: <Int> Balance amount
        """
        response = self.ccxt_inst.contractPrivatePostLinearSwapApiV1SwapCrossAccountPositionInfo(
            params={'margin_account': 'USDT'})
        return float(response['data']['margin_balance'])

    def get_position(self, ticker):
        positions = self.ccxt_inst.contractPrivatePostLinearSwapApiV1SwapCrossPositionInfo(
            params={'contract_code': f'{ticker}-USDT'}
        )['data']

        total = 0
        # long, short 양쪽 모두 position을 갖고 있는 경우가 있음
        for position in positions:
            absolute_amount = float(position['volume']) * self.contract_sizes[ticker]
            if position['direction'] == 'buy':
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
        if self.market == 'USDT':
            symbol = f'{ticker}-USDT'
            params = {
                'contract_code': symbol,
                'volume': int(amount // self.contract_sizes[ticker]),
                'direction': side,
                'offset': open_close,
                'lever_rate': 5,
                'order_price_type': 'optimal_20_ioc'
            }

            res = self.ccxt_inst.contract_private_post_linear_swap_api_v1_swap_cross_order(params=params)
            trade_info = self.ccxt_inst.contract_private_post_linear_swap_api_v1_swap_cross_order_info(params={
                'order_id': res['data']['order_id'],
                'contract_code': symbol
            })
            if trade_info['data'][0]['status'] == '6':
                try:
                    return float(trade_info['data'][0]['trade_avg_price'])
                except:
                    raise Exception(res)

    def get_max_trading_qtys(self):
        """
        :return: {
            'BTC': 120,
            'ETH': 2000,
            ...
        """
        qtys = {}

        res = self.ccxt_inst.contract_private_post_linear_swap_api_v1_swap_order_limit({
            'order_price_type': 'optimal_20_ioc'
        })
        for contract in res['data']['list']:
            ticker = contract['contract_code'].replace('-USDT', '')
            qtys[ticker] = float(contract['open_limit'])

        return qtys

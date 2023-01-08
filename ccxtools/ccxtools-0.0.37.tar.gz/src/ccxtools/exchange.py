from abc import ABCMeta, abstractmethod
from ccxt.base.decimal_to_precision import decimal_to_precision, TRUNCATE


class Exchange(metaclass=ABCMeta):

    def __init__(self, market):
        self.market = market

    @abstractmethod
    def get_contract_sizes(self):
        raise NotImplementedError

    @abstractmethod
    def get_balance(self, ticker):
        raise NotImplementedError

    @abstractmethod
    def get_position(self, ticker: str) -> float:
        raise NotImplementedError

    @abstractmethod
    def post_market_order(self, ticker, side, open_close, amount):
        raise NotImplementedError

    @abstractmethod
    def get_precise_order_amount(self, ticker, ticker_amount):
        """
        :param ticker: <String>
        :param ticker_amount: <Float>
        :return: <Float>
        """
        raise NotImplementedError


class CcxtExchange(Exchange):

    def __init__(self, market):
        super().__init__(market)
        self.ccxt_inst = None
        self.contract_sizes = None

    def get_contract_sizes(self):
        raise NotImplementedError

    def get_balance(self, ticker):
        """
        :param ticker: <String> Ticker name. ex) 'USDT', 'BTC'
        :return: <Int> Balance amount
        """
        return self.ccxt_inst.fetch_balance()[ticker]['total']

    def get_position(self, ticker):
        raise NotImplementedError

    def post_market_order(self, ticker, side, open_close, amount):
        raise NotImplementedError

    def get_precise_order_amount(self, ticker, ticker_amount):
        contract_size = self.contract_sizes[ticker]
        precision = self.ccxt_inst.precision_from_string(str(contract_size))

        return float(decimal_to_precision(ticker_amount, TRUNCATE, precision))

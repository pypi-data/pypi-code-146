from ..classes.ticker import Ticker
from .representation import Representation


class TickerRepresentation(Representation):

    def __init__(self, ticker: Ticker):
        Representation.__init__(self)
        self._symbol = ticker.symbol
        self._price = ticker.price
        self._name = ticker.name
        self._beta = ticker.beta

    def as_dict(self) -> dict:
        return {'symbol': self._symbol,
                'name': self._name,
                'price': self._price,
                'beta': self._beta}

    @staticmethod
    def as_object(dictionary: dict):
        return Ticker(ticker_symbol=dictionary['symbol'],
                      ticker_name=dictionary['name'],
                      price=dictionary['price'],
                      beta=dictionary['beta'])

from typing import Optional


class Ticker:
    def __init__(self, ticker_symbol: str, ticker_name: Optional[str] = None, price: Optional[float] = None,
                 beta: Optional[float] = None):
        self._symbol = ticker_symbol
        self._name = ticker_name
        self._price = price
        self._beta = beta

    @property
    def beta(self):
        return self._beta

    @property
    def symbol(self):
        return self._symbol

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def price(self):
        return self._price

    def __eq__(self, other: 'Ticker'):
        if not isinstance(other, Ticker):
            return False
        return self.symbol == other.symbol

    def __repr__(self):
        return f'{self.symbol}:{self.name}'

    def __str__(self):
        return f'Symbol: {self.symbol}, Name: {self.name}, Price: {self.price}, Beta: {self.beta}'

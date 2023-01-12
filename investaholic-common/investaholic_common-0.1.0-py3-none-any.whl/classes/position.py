from typing import Optional
from .ticker import Ticker
from datetime import datetime


class Position:
    def __init__(self, ticker: Ticker, quantity: float, proposal_code: int = None, closing_date: Optional[datetime] = None):
        self._ticker = ticker
        self._quantity = quantity
        self._closing_date: datetime = closing_date
        self._proposal_code = proposal_code

    @property
    def ticker(self):
        return self._ticker

    @ticker.setter
    def ticker(self, value):
        self._ticker = value

    @property
    def quantity(self):
        return self._quantity

    @property
    def closing_date(self):
        return self._closing_date

    @property
    def proposal_code(self):
        return self._proposal_code

    @proposal_code.setter
    def proposal_code(self, value):
        self._proposal_code = value

    def total_price(self):
        return self.quantity * self.ticker.price

    def __eq__(self, other: 'Position'):
        if not isinstance(other, Position):
            return False
        return self.quantity == other.quantity and self.ticker == other.ticker

    def __repr__(self) -> str:
        return f'{self.ticker}: {self.quantity}'

    def __str__(self) -> str:
        return f'{self.ticker}, Quantity: {self.quantity}, Proposal: {self.proposal_code}'

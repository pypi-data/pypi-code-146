from typing import Optional

from .position import Position
from datetime import datetime


class Proposal:
    def __init__(self, date: datetime, user_id: str, code: Optional[int] = None):
        self._date = date
        self._code = code
        self._user_id = user_id
        self._positions = []

    def add_position(self, position: Position):
        if position not in self._positions:
            self._positions.append(position)

    def total_price(self):
        total_price = 0
        for position in self._positions:
            total_price += position.total_price()

        return total_price

    @property
    def positions(self):
        return self._positions

    @property
    def date(self):
        return self._date

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def user_id(self):
        return self._user_id

    def __repr__(self):
        return f'Proposal: {self.date} -> {self.positions}'

    def __str__(self) -> str:
        fmt = f'Proposal nr. {self.code}, investment starting: {self.date.strftime("%d.%m.%Y")}, ' \
              f'user: {self.user_id}, Total proposal: {self.total_price()}\n\t Positions:\n'
        for pos in self.positions:
            fmt += f'\t\t{pos}\n'
        return fmt



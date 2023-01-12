from .representation import Representation
from ..classes.position import Position
from .ticker_representation import TickerRepresentation
import datetime as dt

class PositionRepresentation(Representation):
    def __init__(self, position: Position):
        Representation.__init__(self)
        self._ticker = position.ticker
        self._qty = position.quantity
        self._closing_date = position.closing_date
        self._proposal_code = position.proposal_code

    def as_dict(self) -> dict:
        closing_date = self._closing_date.strftime('%Y-%m-%d') if self._closing_date is not None else None
        return {'ticker': TickerRepresentation(self._ticker).as_dict(),
                'quantity': self._qty,
                'closing_date': closing_date,
                'proposal_code': self._proposal_code}

    @staticmethod
    def as_object(dictionary: dict) -> Position:
        return Position(ticker=TickerRepresentation.as_object(dictionary['ticker']),
                        closing_date=dt.datetime.strptime(dictionary['closing_date'], '%Y-%m-%d') if dictionary['closing_date'] is not None else None,
                        quantity=dictionary['quantity'],
                        proposal_code=dictionary['proposal_code'])
from .representation import Representation
from ..classes.proposal import Proposal
from .position_representation import PositionRepresentation
import datetime as dt

class ProposalRepresentation(Representation):
    _FMT = '%Y-%m-%d'

    def __init__(self, proposal: Proposal):
        Representation.__init__(self)
        self._code = proposal.code
        self._date = proposal.date
        self._positions = proposal.positions
        self._user_id = proposal.user_id

    def as_dict(self) -> dict:
        return {'code': self._code,
                'start_date': dt.datetime.strftime(self._date, self._FMT),
                'positions': [PositionRepresentation(position).as_dict() for position in
                              self._positions],
                'user_id': self._user_id}

    @classmethod
    def as_object(cls, dictionary: dict) -> Proposal:
        start_date = dt.datetime.strptime(dictionary['start_date'], cls._FMT)
        proposal = Proposal(date=start_date,
                            code=dictionary['code'],
                            user_id=dictionary['user_id'])

        for position in dictionary['positions']:
            proposal.add_position(PositionRepresentation.as_object(position))
        return proposal

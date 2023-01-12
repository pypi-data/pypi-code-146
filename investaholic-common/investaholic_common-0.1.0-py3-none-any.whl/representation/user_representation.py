from .representation import Representation
from ..classes.user import User

from investaholic_common.classes.risk import Risk

class UserRepresentation(Representation):
    def __init__(self, user: User):
        Representation.__init__(self)
        self._id = user.id
        self._surname = user.surname
        self._name = user.name
        self._risk = user.risk
        self._capital = user.capital

    def as_dict(self) -> dict:
        return {'id': self._id,
                'name': self._name,
                'surname': self._surname,
                'capital': self._capital,
                'risk': self._risk.value}

    @staticmethod
    def as_object(dictionary: dict):
        return User(name=dictionary['name'],
                    surname=dictionary['surname'],
                    id_=dictionary['id'],
                    # risk=Risk(dictionary['risk']),
                    risk=dictionary['risk'],
                    capital=dictionary['capital'])

from .risk import Risk

class User:
    def __init__(self, name: str, surname: str, id_: str, risk: Risk, capital: float):
        self._name = name
        self._surname = surname
        self._id = id_
        self._risk = risk
        self._capital = capital

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def risk(self):
        return self._risk

    @property
    def capital(self):
        return self._capital

    @property
    def surname(self):
        return self._surname

    def __eq__(self, other: 'User'):
        if not isinstance(other, User):
            return False

        return self.id == other.id

    def __repr__(self):
        return f'User {self.id} -> {self.name}:{self.surname}'

    def __str__(self):
        return f'User ID: {self.id}, name: {self.name}, surname: {self.surname}'

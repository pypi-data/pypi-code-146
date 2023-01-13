"""NBA game status"""

from enum import Enum

class NbaGameExtendedStatus(str, Enum):
    REGULAR = 'regular'
    POSTPONED = 'postponed'

    @classmethod
    def match(cls, status_number: int) -> 'NbaGameExtendedStatus':
        if status_number == 0: return cls.REGULAR
        elif status_number == 2: return cls.POSTPONED
        return cls.REGULAR

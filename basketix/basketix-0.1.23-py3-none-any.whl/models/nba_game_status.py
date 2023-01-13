"""NBA game status"""

from enum import Enum

class NbaGameStatus(str, Enum):
    UNPLAYED = 'unplayed'
    UNSTARTED = 'unstarted'
    INPROGRESS = 'inProgress'
    FINISHED = 'finished'

    @classmethod
    def match(cls, status_number: int) -> 'NbaGameStatus':
        if status_number == 0: return cls.UNPLAYED
        elif status_number == 1: return cls.UNSTARTED
        elif status_number == 2: return cls.INPROGRESS
        elif status_number == 3: return cls.FINISHED
        return cls.UNSTARTED

NbaGameStatusType = NbaGameStatus

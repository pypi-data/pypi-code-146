"""NBA game status"""

from enum import Enum

class NbaGameLocation(str, Enum):
    HOME = 'home'
    AWAY = 'away'

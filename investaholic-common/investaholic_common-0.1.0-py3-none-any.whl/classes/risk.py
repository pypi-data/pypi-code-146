import enum
from investaholic_common.classes.ticker import Ticker


class Risk(enum.Enum):
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5

    @classmethod
    def get_risk(cls, ticker: Ticker, boundaries: tuple) -> 'Risk':
        if len(boundaries) != 4:
            raise ValueError(f'Just 4 boundaries should be specified. {len(boundaries)} given.')

        beta = ticker.beta

        if beta < boundaries[0]:
            return cls.VERY_LOW
        elif boundaries[0] <= beta < boundaries[1]:
            return cls.LOW
        elif boundaries[1] <= beta < boundaries[2]:
            return cls.MEDIUM
        elif boundaries[2] <= beta < boundaries[3]:
            return cls.HIGH
        else:
            return cls.VERY_HIGH
543
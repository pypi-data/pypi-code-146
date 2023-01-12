from enum import Enum, unique
from typing import Optional


@unique
class AccessMode(Enum):
    SINGLE = "single"
    RECURRENT = "recurrent"


@unique
class TaxReturnType(Enum):
    YEARLY = "yearly"
    MONTHLY = "monthly"


@unique
class TaxRetentionType(Enum):
    INFLOW = "inflow"
    OUTFLOW = "outflow"


@unique
class Environment(Enum):
    SANDBOX = "https://sandbox.belvo.com"
    DEVELOPMENT = "https://development.belvo.com"
    PRODUCTION = "https://api.belvo.com"

    @classmethod
    def get_url(cls, environment: Optional[str]):
        if not environment:
            return None

        try:
            return cls[environment.upper()].value
        except KeyError:
            return environment

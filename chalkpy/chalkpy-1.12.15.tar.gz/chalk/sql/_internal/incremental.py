import dataclasses
from datetime import timedelta
from typing import Optional


@dataclasses.dataclass
class IncrementalSettings:
    mode: str = "row"  # "row" or "group" or "parameter"
    lookback_period: Optional[timedelta] = None
    incremental_column: Optional[str] = None

import dataclasses
from typing import Dict, List, Union


@dataclasses.dataclass
class KrakenMessage:
    error: List[str]
    result: Union[List, Dict]

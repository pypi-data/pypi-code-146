from dataclasses import asdict, dataclass, field
from typing import List

from gandai.models.Search import Search


@dataclass(order=True)
class Target:
    key: str = field(init=False)  # primary key
    search_key: str  #
    domain: str  # unique
    owner: list

    @property
    def current_owner(self):
        return self.owner[0]


def load_targets(search_key: str) -> List[Search]:
    return []

from dataclasses import asdict, dataclass, field
from enum import Enum
from time import time
from typing import Optional

from gandai.datastore import Cloudstore

ds = Cloudstore()


class EventType(str, Enum):
    CREATE = "create"
    ADVANCE = "advance"
    QUALIFY = "qualify"
    REJECT = "reject"
    # FoobarEnum


@dataclass
class Event:
    key: str = field(init=False)
    search_key: str
    # target_key: Optional[str]  # null for a query event
    domain: str

    actor_key: str  #
    ## todo: enums in dataclasses
    type: str  # build, advance, qualify, reject, conflict
    created: int = field(init=False)

    def __post_init__(self):
        # build, advance, qualify, reject, conflict
        self.created = int(time())
        self.key = f"searches/{self.search_key}/events/{self.created}"


def post_event(actor_key: str, search_key: str, domain: str, type: str) -> None:
    event = Event(actor_key=actor_key, search_key=search_key, domain=domain, type=type)
    ds[event.key] = asdict(event)
    return f"posted: {event.key}"

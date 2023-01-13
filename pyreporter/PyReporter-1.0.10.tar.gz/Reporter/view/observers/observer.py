from ...events.out_event import OutEvent
from typing import Any


class Observer:
    # notify(target): Updates the observer based off 'target'
    def notify(self, target: Any):
        pass

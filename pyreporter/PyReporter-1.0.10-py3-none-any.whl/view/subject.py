from .observers.observer import Observer
from ..events.out_event import OutEvent
from typing import Optional


# Subject: Abstract Subject for Observer Design Model
class Subject:
    def __init__(self):
        self.observers = []


    # attach(observer): Adds an observer
    def attach(self, observer: Observer):
        self.observers.append(observer)


    # detach(observer): Removes an observer
    def detach(self, observer: Observer):
        observer_len = len(self.observers)

        for i in range(observer_len):
            current_observer = self.observer[i]
            if (self.observers[i] == observer):
                self.observers.pop(i)


    # notify(out_event): Notifies all observers
    def notify(self, out_event: OutEvent):
        for o in self.observers:
            o.notify(out_event)

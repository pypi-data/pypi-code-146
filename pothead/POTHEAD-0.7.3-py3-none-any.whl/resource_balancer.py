from itertools import chain
from random import shuffle
from threading import Condition, Lock
from typing import Iterable
from math import inf


class Resource:
    def __init__(self, resource):
        self.resource = resource
        self.usage = 0

    def __cmp__(self, other):
        return self.usage.__cmp__(other.usage)

    def __lt__(self, other):
        return self.usage.__lt__(other.usage)


class ResourceLoan:
    def __init__(self, balancer, instance):
        self._lock = Lock()
        self._balancer = balancer
        self._instance = instance

    def __enter__(self):
        return self._instance.resource

    def release(self):
        with self._lock:
            if self._balancer:
                self._balancer._release(self._instance)
                self._balancer = None

    def __exit__(self, type, value, traceback):
        self.release()


class BoundedResourceBalancer:
    def __init__(self, bound=inf):
        self._active = list()
        self._ghosts = list()
        self._condition = Condition()
        self.bound = bound

    def _available(self):
        available = (r for r in self._active if r.usage < self.bound)
        return next(available, None)

    def active_count(self):
        return len(self._active)

    def acquire(self) -> ResourceLoan:
        with self._condition:
            winner = self._condition.wait_for(self._available)
            winner.usage += 1
            self._active.sort()
            return ResourceLoan(self, winner)

    def _release(self, instance):
        with self._condition:
            instance.usage -= 1
            self._active.sort()
            self._condition.notify_all()

    def provision(self, resources: Iterable[object]):
        with self._condition:
            new_resources = set(resources)

            active, ghosts = self._active, self._ghosts
            self._ghosts = []
            self._active = []

            for instance in chain(active, ghosts):
                try:
                    new_resources.remove(instance.resource)
                    self._active.append(instance)
                except KeyError:
                    if instance.usage > 0:
                        self._ghosts.append(instance)

            for new_resource in new_resources:
                self._active.append(Resource(new_resource))

            shuffle(self._active)
            self._active.sort()
            self._condition.notify_all()

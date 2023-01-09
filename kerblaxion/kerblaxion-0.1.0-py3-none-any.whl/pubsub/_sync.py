
from typing import Any, Awaitable, Callable, Collection, Generic, Optional, ParamSpec

P = ParamSpec('P')

Subscriber = Callable[P, Any]

class Publisher(Generic[P]):
  def __init__(self, subscribers: Optional[Collection[Subscriber[P]]] = None):
    self.subscribers = [] if subscribers is None else list(subscribers)

  def add(self, s: Subscriber[P]):
    self.subscribers.append(s)

  def remove(self, s: Subscriber[P]):
    self.subscribers.remove(s)

  def __call__(self, *args: P.args, **kwargs: P.kwargs):
    for s in self.subscribers:
      s(*args, **kwargs)

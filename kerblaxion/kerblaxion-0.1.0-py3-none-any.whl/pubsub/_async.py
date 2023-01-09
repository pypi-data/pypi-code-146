
from typing import Any, Awaitable, Callable, Collection, Generic, Optional, ParamSpec

import asyncio

P = ParamSpec('P')

AsyncSubscriber = Callable[P, Awaitable[Any]]

class AsyncPublisher(Generic[P]):
  def __init__(self, subscribers: Optional[Collection[AsyncSubscriber[P]]] = None):
    self.subscribers = [] if subscribers is None else list(subscribers)

  def add(self, s: AsyncSubscriber[P]):
    self.subscribers.append(s)

  def remove(self, s: AsyncSubscriber[P]):
    self.subscribers.remove(s)

  async def __call__(self, *args: P.args, **kwargs: P.kwargs):
    await asyncio.gather(*[
      s(*args, **kwargs) for s in self.subscribers
    ])


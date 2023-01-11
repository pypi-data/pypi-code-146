from typing import Iterable, List, Type
from queue import Queue
from pyoptional.pyoptional import PyOptional

from ..common.perception import Perception


class Sensor():
    def __init__(self, subscribed_events: List[Type]=[]) -> None:
        self.__perception_buffer: Queue[Perception] = Queue()

        if subscribed_events is None:
            raise ValueError("Cannot subscribe to a `None` list of event types.")
        elif not isinstance(subscribed_events, List):
            raise ValueError("Cannot subscribe to something which is not a list of event types.")
        elif not all([isinstance(event_type, Type) and issubclass(event_type, Perception) for event_type in subscribed_events]):
            raise ValueError("Cannot subscribe to something which is not a type of `Perception`.")
        else:
            self.__subscribed_events: List[Type] = subscribed_events

    def subscribe_to_event_type(self, event_type: Type) -> None:
        if event_type is None:
            raise ValueError("Cannot subscribe to a `None` event type.")
        elif not isinstance(event_type, Type) or not issubclass(event_type, Perception):
            raise ValueError("Cannot subscribe to something which is not a type of `Perception`.")
        elif event_type not in self.__subscribed_events:  # We do not want to re-subscribe.
            self.__subscribed_events.append(event_type)

    def unsubscribe_from_event_type(self, event_type: Type) -> None:
        if event_type is None:
            raise ValueError("Cannot unsubscribe from a `None` event type.")
        if not isinstance(event_type, Type) or not issubclass(event_type, Perception):
            raise ValueError("Cannot unsubscribe from something which is not a type of `Perception`.")
        elif event_type in self.__subscribed_events:
            self.__subscribed_events.remove(event_type)

    def is_subscribed_to(self, event_type: Type) -> bool:
        return event_type in self.__subscribed_events

    def sink(self, perception: Perception) -> None:
        if perception is None:
            raise ValueError("Cannot sink a `None` `Perception`.")
        elif self.is_subscribed_to(type(perception)):
            self.__perception_buffer.put(perception)
        else:
            raise ValueError("Cannot sink a `Perception` which this `Sensor` is not subscribed to.")

    def has_perception(self) -> bool:
        return not self.__perception_buffer.empty()

    def source(self) -> PyOptional[Perception]:
        if not self.__perception_buffer.empty():
            return PyOptional.of(self.__perception_buffer.get())
        else:
            return PyOptional.empty()

    def source_all(self) -> Iterable[Perception]:
        while not self.__perception_buffer.empty():
            yield self.__perception_buffer.get()

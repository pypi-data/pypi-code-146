from typing import List, Union

from rispack.events import BaseEvent
from rispack.schemas import BaseSchema
from rispack.stores import scoped_session


class BaseAction:
    def __init__(self):
        self.events: List[BaseEvent] = []

    def publish(self, event: BaseEvent, payload: Union[dict, BaseSchema]):
        event_to_publish = event.load(payload)

        self.events.append(event_to_publish)

    @classmethod
    def run(cls, params):
        action = cls()

        action_response = action._scoped(params)

        if len(action.events):
            for event in action.events:
                event.publish()

            action.events = []

        return action_response

    @scoped_session
    def _scoped(self, params):
        return self.call(params)

    def call(self):
        raise NotImplementedError

from functools import wraps
from json import JSONDecodeError
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from ddtrace import tracer
from marshmallow import Schema, ValidationError

from dh_potluck.messaging import Message
from dh_potluck.messaging.batching_consumer import BatchingMessageConsumer

BatchingMessagesHandler = Callable[[str, str, List[Message]], Optional[bool]]


class NoBatchingHandlerException(Exception):
    def __init__(self, key, available_handlers):
        self.key = key
        self.message = f'No batching handler for: {key}. Available handlers: {available_handlers}'
        super().__init__(self.message)


class BatchingMessageConsumerApp:
    _handlers: Dict[Tuple[str, str], BatchingMessagesHandler]

    def __init__(self, batching_consumer: BatchingMessageConsumer):
        self._consumer = batching_consumer
        self._handlers = {}

    def register(
        self, topic: str, message_type: str
    ) -> Callable[[BatchingMessagesHandler], BatchingMessagesHandler]:
        def decorator_register_message_handler(func: BatchingMessagesHandler):
            self.register_handler(topic, message_type, func)
            return func

        return decorator_register_message_handler

    def register_handler(self, topic, message_type, handler: BatchingMessagesHandler) -> None:
        self._handlers[(topic, message_type)] = handler

    def run(self) -> None:
        """
        Start consuming messages.
        """

        for batch in self._consumer.get_batches():
            self._handle_batch(batch)

    def _handle_batch(self, batch: List[Message]) -> None:
        batches_by_topic_and_type: Dict[Tuple[str, str], List[Message]] = {}
        for message in batch:
            topic = message.topic()
            message_type = message.value()['message_type']
            batches_by_topic_and_type.setdefault((topic, message_type), []).append(message)

        for (topic, message_type), messages in batches_by_topic_and_type.items():
            should_commit = self._handle_one_topic_batch(topic, message_type, messages)
            if not self._consumer.auto_commit and should_commit:
                self._consumer.commit(messages=messages)

    def _handle_one_topic_batch(
        self,
        topic: str,
        message_type: str,
        messages: List[Message],
    ) -> bool:
        handler = self._get_handler(topic, message_type)
        with tracer.trace('kafka.batch_consume', resource=f'{topic} {message_type}') as span:
            span.set_tag('batch_size', len(messages))
            should_commit = handler(topic, message_type, messages)
            return should_commit is not False

    def _get_handler(self, topic: str, message_type: str) -> BatchingMessagesHandler:
        key = (topic, message_type)
        handler = self._handlers.get(key)
        if not handler:
            raise NoBatchingHandlerException(key, list(self._handlers))
        return handler


def validate_schema_per_message(schema: Schema):
    def _wrapper(handler: Callable[[str, str, List[Any], List[Message]], Optional[bool]]):
        @wraps(handler)
        def wrapper(topic: str, message_type: str, messages: List[Message]) -> Optional[bool]:
            payloads = [schema.loads(message.value()['payload']) for message in messages]
            return handler(topic, message_type, payloads, messages)

        return wrapper

    return _wrapper


def validate_schema_per_message_and_ignore_errors(schema: Schema):
    def _wrapper(
        handler: Callable[
            [str, str, List[Any], List[Union[ValidationError, JSONDecodeError]], List[Message]],
            Optional[bool],
        ]
    ):
        @wraps(handler)
        def wrapper(topic: str, message_type: str, messages: List[Message]) -> Optional[bool]:
            payloads = []
            errors = []
            for message in messages:
                try:
                    payloads.append(schema.loads(message.value()['payload']))
                except (ValidationError, JSONDecodeError) as e:
                    errors.append(e)
            return handler(topic, message_type, payloads, errors, messages)

        return wrapper

    return _wrapper

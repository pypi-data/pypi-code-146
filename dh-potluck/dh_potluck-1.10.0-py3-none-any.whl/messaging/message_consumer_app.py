import logging
from typing import Optional

from marshmallow import Schema

from dh_potluck.messaging import IncomingMessageRouter, MessageHandler, MessageHandlerCallback
from dh_potluck.messaging.typings import ConsumerConfig

LOG = logging.getLogger(__name__)


_HANDLERS = {}


def message_handler(topic: str, schema: Schema):
    """
    Registers this function as a message handler
    :param str topic: Topic to handle
    :param Schema schema: Schema to use to deserialize the message payload
    """

    def decorator_register_message_handler(func: MessageHandlerCallback):
        _HANDLERS[topic] = MessageHandler(schema, func)
        return func

    return decorator_register_message_handler


class MessageConsumerApp(object):

    _router: IncomingMessageRouter

    def __init__(
        self,
        consumer_group: str,
        config_overrides: Optional[ConsumerConfig] = None,
        brokers: Optional[str] = None,
        should_connect_ssl: Optional[bool] = None,
    ):
        """
        :param str consumer_group: The kafka consumer group to use
        :param dict config_overrides: Any kafka configuration overrides
        :param str brokers: list of brokers to connect to (also can be provided via the flask
            config `KAFKA_BROKERS_LIST`)
        :param bool should_connect_ssl: if a ssl connection should be used to kafka (also can be
            provided via the flask config `KAFKA_USE_SSL_CONNECTION`)
        """
        self._router = IncomingMessageRouter(
            _HANDLERS, consumer_group, config_overrides, brokers, should_connect_ssl
        )

    def register(self, topic: str, schema: Schema):
        """
        Registers decorated function as a message handler
        :param str topic: Topic to handle
        :param Schema schema: Schema to use to deserialize the message payload
        """

        def decorator_register_message_handler(func: MessageHandlerCallback):
            self.register_handler(topic, schema, func)
            return func

        return decorator_register_message_handler

    def register_handler(self, topic: str, schema: Schema, handler: MessageHandlerCallback) -> None:
        self._router.register_handler(topic, schema, handler)

    def run(self):
        """
        Start consuming messages. On new messages, use the registered message_handler to handle it.
        :return: None
        """
        self._router.run()

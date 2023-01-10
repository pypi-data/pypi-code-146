import logging
import time
from typing import Callable, NamedTuple, Optional, Union

from pika import PlainCredentials, BlockingConnection, ConnectionParameters, BasicProperties
from pika.exceptions import AMQPConnectionError, AMQPChannelError, ConnectionClosedByBroker


class RabbitMQConfig(NamedTuple):
    HOST: str
    PORT: int = 5672
    USER: str = ''
    PSW: str = ''
    VIR_HOST: str = ''
    HEART_BEAT: Optional[int] = None
    SOCKET_TIMEOUT: Union[int, float] = 10
    BLOCKET_CONNECTION_TIMEOUT: Union[int, float] = None
    SHORT_CONNECT: bool = True  # 短连接模式


class RabbitMQAccessor:

    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.client = None
        self.callbacks = {}

    def __del__(self):
        self.close()

    def close(self):
        try:
            if self.is_connected():
                self.client.close()
        finally:
            self.client = None

    def get_client(self):
        if self.client is None:
            if self.config.USER is not None and self.config.PSW is not None and len(self.config.USER) > 0:
                credentials = PlainCredentials(self.config.USER, self.config.PSW)
                self.client = BlockingConnection(ConnectionParameters(host=self.config.HOST, port=self.config.PORT, virtual_host=self.config.VIR_HOST, credentials=credentials, socket_timeout=self.config.SOCKET_TIMEOUT, heartbeat=self.config.HEART_BEAT, blocked_connection_timeout=self.config.BLOCKET_CONNECTION_TIMEOUT))
            else:
                self.client = BlockingConnection(ConnectionParameters(host=self.config.HOST, port=self.config.PORT, virtual_host=self.config.VIR_HOST, socket_timeout=self.config.SOCKET_TIMEOUT, heartbeat=self.config.HEART_BEAT, blocked_connection_timeout=self.config.BLOCKET_CONNECTION_TIMEOUT))
        return self.client

    def is_connected(self) -> bool:
        if self.client and self.client.is_open:
            return True
        return False

    def set_call_result(self, call_method: str, **kwargs):
        if isinstance(self.callbacks, dict):
            call_method = self.callbacks.get(call_method)
            if isinstance(call_method, Callable):
                call_method(**kwargs)

    def enable_logging(self, enable_log: bool, callback: Callable = None):
        if enable_log is True:
            self.callbacks['debug_log'] = callback
        else:
            self.callbacks['debug_log'] = None

    def publish_exchange(self, exchange: str, routing_key: str, message: str, exchange_type: str = 'topic', **kwargs):
        client = self.get_client()
        if client is not None:
            try:
                channel = client.channel()
                channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=kwargs.get('durable', True))
                channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message, properties=BasicProperties(delivery_mode=kwargs.get('delivery_mode', 2), ))
                channel.close()
                return True
            finally:
                if self.config.SHORT_CONNECT is True or self.is_connected() is False:
                    self.close()

    def publish_queue(self, queue_name: str, message: str, exchange: str = '', **kwargs):
        client = self.get_client()
        if client is not None:
            try:
                channel = client.channel()
                channel.queue_declare(queue=queue_name, durable=kwargs.get('durable', True))
                channel.basic_publish(exchange=exchange, routing_key=queue_name, body=message, properties=BasicProperties(delivery_mode=kwargs.get('delivery_mode', 2), ))
                channel.close()
                return True
            finally:
                if self.config.SHORT_CONNECT is True or self.is_connected() is False:
                    self.close()

    def consume_exchange(self, exchange: str, exchange_type: str = 'topic', routing_key: str = '#', retry_interval: int = 10, callback: Callable = None, consumer_tag: Optional[str] = None, **kwargs):
        self.callbacks['receive_data'] = callback

        def real_callback(c, method, properties, body):
            c.basic_ack(delivery_tag=method.delivery_tag)
            self.set_call_result('receive_data', body=body)

        while True:
            try:
                connection = self.get_client()
                channel = connection.channel()
                channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=kwargs.get('durable', True))  # 声明一个Exchange
                channel.queue_declare(queue=exchange, exclusive=kwargs.get('exclusive', True))  # 声明一个队里
                channel.queue_bind(exchange=exchange, queue=exchange, routing_key=routing_key)  # 绑定一个队列
                channel.basic_consume(exchange, on_message_callback=real_callback, consumer_tag=consumer_tag)
                channel.start_consuming()
            except ConnectionClosedByBroker as e:
                logging.error(f'exchange={exchange} ConnectionClosedByBroker({e.__str__()})')
            except AMQPChannelError as e:
                logging.error(f'exchange={exchange} AMQPChannelError({e.__str__()})')
            except AMQPConnectionError as e:
                logging.error(f'exchange={exchange} AMQPConnectionError({e.__str__()})')
            except Exception as e:
                logging.error(f'exchange={exchange} exception({e.__str__()})')
            finally:
                self.close()
            time.sleep(retry_interval)

    def consume_queue(self, queue_name: str, retry_interval: int = 10, callback: Callable = None, consumer_tag: Optional[str] = None, **kwargs):
        self.callbacks['receive_data'] = callback

        def real_callback(c, method, properties, body):
            c.basic_ack(delivery_tag=method.delivery_tag)
            self.set_call_result('receive_data', body=body)

        while True:
            try:
                connection = self.get_client()
                channel = connection.channel()
                channel.queue_declare(queue=queue_name, durable=kwargs.get('durable', True))
                channel.basic_qos(prefetch_count=kwargs.get('prefetch_count', 1))
                channel.basic_consume(queue=queue_name, consumer_tag=consumer_tag, on_message_callback=real_callback)
                channel.start_consuming()
            except ConnectionClosedByBroker as e:
                logging.error(f'queue_name={queue_name} ConnectionClosedByBroker({e.__str__()})')
            except AMQPChannelError as e:
                logging.error(f'queue_name={queue_name} AMQPChannelError({e.__str__()})')
            except AMQPConnectionError as e:
                logging.error(f'queue_name={queue_name} AMQPConnectionError({e.__str__()})')
            except Exception as e:
                logging.error(f'queue_name={queue_name} exception({e.__str__()})')
            finally:
                self.close()
            time.sleep(retry_interval)

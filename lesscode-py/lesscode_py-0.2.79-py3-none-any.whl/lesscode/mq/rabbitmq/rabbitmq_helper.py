# -*- coding: utf-8 -*-
# @Time    : 2022/8/23 14:40
# @Author  : navysummer
# @Email   : navysummer@yeah.net
import logging
import traceback

import pika
from tornado.options import options


class RabbitMqHelper:
    def __init__(self, **kwargs):
        if kwargs.get("host"):
            host = kwargs.pop("host")
        else:
            host = options.rabbitmq_config.get("host", "127.0.0.1")
        if kwargs.get("port"):
            port = kwargs.pop("port")
        else:
            port = options.rabbitmq_config.get("port", 5672)
        if kwargs.get("username"):
            username = kwargs.pop("username")
        else:
            username = options.rabbitmq_config.get("username")
        if kwargs.get("password"):
            password = kwargs.pop("password")
        else:
            password = options.rabbitmq_config.get("password")
        if kwargs.get("queue"):
            self.queue = kwargs.pop("queue")
        else:
            raise Exception("missing queue")
        self.exchange = kwargs.pop("exchange", None)
        exchange_kwargs = kwargs.pop("exchange_kwargs", {})
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=credentials, **kwargs))
        self.channel = self.connection.channel()
        queue_kwargs = kwargs.get("queue_kwargs", {})
        self.channel.queue_declare(queue=self.queue, durable=True, **queue_kwargs)
        if self.exchange:
            self.channel.exchange_declare(exchange=self.exchange, **exchange_kwargs)

    def publish(self, message: str, exchange="", **kwargs):
        if isinstance(message, str):
            message = message.encode("utf-8")
        elif not isinstance(message, bytes):
            raise Exception("message must be str or bytes")
        res = self.channel.basic_publish(exchange=exchange, routing_key=self.queue, body=message,
                                         properties=pika.BasicProperties(
                                             delivery_mode=2
                                         ), **kwargs)
        logging.info(f"send message={message.decode('utf-8')} to queue={self.queue}")
        self.connection.close()
        data = {"message": message, "queue": self.queue, "res": res}
        return data

    def consume(self, callback, **kwargs):
        logging.info("Waiting for messages")
        self.channel.basic_consume(queue=self.queue, on_message_callback=callback, **kwargs)
        try:
            self.channel.start_consuming()
        except Exception:
            logging.error(traceback.format_exc())

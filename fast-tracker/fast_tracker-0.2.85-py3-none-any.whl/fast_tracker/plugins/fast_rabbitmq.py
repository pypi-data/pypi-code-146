#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from fast_tracker import Layer, ComponentType
from fast_tracker.trace import tags
from fast_tracker.trace.carrier import Carrier
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag


def install():
    from pika.channel import Channel

    _basic_publish = Channel.basic_publish
    __on_deliver = Channel._on_deliver
    Channel.basic_publish = _fast_basic_publish_func(_basic_publish)
    Channel._on_deliver = _fast__on_deliver_func(__on_deliver)


def _fast_basic_publish_func(_basic_publish):
    def _fast_basic_publish(this, exchange, routing_key, body, properties=None, mandatory=False):
        peer = "%s:%s" % (this.connection.params.host, this.connection.params.port)
        context = get_context()
        import pika

        with context.new_exit_span(
            op="RabbitMQ/Topic/" + exchange + "/Queue/" + routing_key + "/Producer" or "/", peer=peer
        ) as span:
            carrier = span.inject()
            span.layer = Layer.MQ
            span.component = ComponentType.RabbitmqProducer
            properties = pika.BasicProperties() if properties is None else properties

            if properties.headers is None:
                properties.headers = {}
            for item in carrier:
                properties.headers[item.key] = item.val

            res = _basic_publish(this, exchange, routing_key, body, properties=properties, mandatory=mandatory)
            span.tag(Tag(key=tags.MqType, val=ComponentType.Rabbitmq))
            span.tag(Tag(key=tags.MqBroker, val=peer))
            span.tag(Tag(key=tags.MqTopic, val=exchange))
            span.tag(Tag(key=tags.MqQueue, val=routing_key))

            return res

    return _fast_basic_publish


def _fast__on_deliver_func(__on_deliver):
    def _fast__on_deliver(this, method_frame, header_frame, body):
        peer = "%s:%s" % (this.connection.params.host, this.connection.params.port)
        context = get_context()
        exchange = method_frame.method.exchange
        routing_key = method_frame.method.routing_key
        carrier = Carrier()
        for item in carrier:
            if item.key in header_frame.properties.headers:
                item.val = header_frame.properties.headers[item.key]

        with context.new_entry_span(
            op="RabbitMQ/Topic/" + exchange + "/Queue/" + routing_key + "/Consumer" or "", carrier=carrier
        ) as span:
            span.layer = Layer.MQ
            span.component = ComponentType.RabbitmqConsumer
            __on_deliver(this, method_frame, header_frame, body)
            span.tag(Tag(key=tags.MqType, val=ComponentType.Rabbitmq))
            span.tag(Tag(key=tags.MqBroker, val=peer))
            span.tag(Tag(key=tags.MqTopic, val=exchange))
            span.tag(Tag(key=tags.MqQueue, val=routing_key))

    return _fast__on_deliver

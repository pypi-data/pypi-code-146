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
    from kafka import KafkaProducer
    from kafka import KafkaConsumer

    _send = KafkaProducer.send
    __poll_once = KafkaConsumer._poll_once
    KafkaProducer.send = _fast_send_func(_send)
    KafkaConsumer._poll_once = _fast__poll_once_func(__poll_once)


def _fast__poll_once_func(__poll_once):
    def _fast__poll_once(this, timeout_ms, max_records, update_offsets=True):
        res = __poll_once(this, timeout_ms, max_records, update_offsets=update_offsets)
        if res:
            try:
                # bootstrap_servers 一般会给列表类型数据
                brokers = (
                    ";".join(this.config["bootstrap_servers"])
                    if type(this.config["bootstrap_servers"]) == list
                    else this.config["bootstrap_servers"]
                )
                context = get_context()
                topics = ";".join(
                    this._subscription.subscription or [t.topic for t in this._subscription._user_assignment]
                )
                with context.new_entry_span(
                    op="Kafka/" + topics + "/Consumer/" + (this.config["group_id"] or "")
                ) as span:
                    for consumerRecords in res.values():
                        for record in consumerRecords:
                            carrier = Carrier()
                            for item in carrier:
                                for header in record.headers:
                                    if item.key == header[0]:
                                        # 兼容kafka-python 2.0.1 和 2.0.2 两个版本
                                        # item.val = str(header[1])
                                        item.val = header[1].decode("utf-8")

                            span.extract(carrier)
                        span.tag(Tag(key=tags.MqType, val=ComponentType.Kafka))
                        span.tag(Tag(key=tags.MqBroker, val=brokers))
                        span.tag(Tag(key=tags.MqTopic, val=topics))
                        span.layer = Layer.MQ
                        span.component = ComponentType.KafkaConsumer
            except Exception as e:
                print(str(e))

        return res

    return _fast__poll_once


def _fast_send_func(_send):
    def _fast_send(this, topic, value=None, key=None, headers=None, partition=None, timestamp_ms=None):
        # bootstrap_servers 一般会给列表类型数据
        peer = (
            ";".join(this.config["bootstrap_servers"])
            if type(this.config["bootstrap_servers"]) == list
            else this.config["bootstrap_servers"]
        )
        context = get_context()
        with context.new_exit_span(op="Kafka/" + topic + "/Producer" or "/", peer=peer) as span:
            carrier = span.inject()
            span.layer = Layer.MQ
            span.component = ComponentType.KafkaProducer

            if headers is None:
                headers = []
            for item in carrier:
                headers.append((item.key, item.val.encode("utf-8")))

            res = _send(
                this, topic, value=value, key=key, headers=headers, partition=partition, timestamp_ms=timestamp_ms
            )
            span.tag(Tag(key=tags.MqType, val=ComponentType.Kafka))
            span.tag(Tag(key=tags.MqBroker, val=peer))
            span.tag(Tag(key=tags.MqTopic, val=topic))

            return res

    return _fast_send

#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

import time
from collections import namedtuple
from enum import Enum
from typing import List

version = '3.1.18'
version_info = list(map(int, version.split('.')))


class Component(Enum):
    Unknown = 0
    General = 7000  # built-in modules that may not have a logo to display
    Flask = 7001
    Requests = 7002
    PyMysql = 7003
    Django = 7004
    Tornado = 7005
    Redis = 7
    MongoDB = 9
    KafkaProducer = 40
    KafkaConsumer = 41
    RabbitmqProducer = 52
    RabbitmqConsumer = 53
    Elasticsearch = 47
    Urllib3 = 7006
    Sanic = 7007
    AioHttp = 7008
    Pyramid = 7009


class ComponentType():
    Unknown = "Unknown"
    General = "General"  # built-in modules that may not have a logo to display
    Flask = "Flask"
    Falcon = "Falcon"
    Requests = "Requests"
    PyMysql = "PyMysql"
    Django = "Django"
    Tornado = "Tornado"
    Redis = "Redis"
    MongoDB = "MongoDB"
    Kafka = "Kafka"
    KafkaProducer = "KafkaProducer"
    KafkaConsumer = "KafkaConsumer"
    Rabbitmq = "Rabbitmq"
    RabbitmqProducer = "RabbitmqProducer"
    RabbitmqConsumer = "RabbitmqConsumer"
    Elasticsearch = "ElasticSearch"
    Urllib3 = "Urllib3"
    Sanic = "Sanic"
    AioHttp = "AioHttp"
    Pyramid = "Pyramid"
    CustomEvent = "CustomEvent"
    Log = "Log"
    RQ = "RQ"


class Layer(Enum):
    Local = 0
    Database = 1
    RPCFramework = 2
    Http = 3
    MQ = 4
    Cache = 5
    User = 6
    Log = 7


class Kind(Enum):
    Local = 0
    Entry = 1
    Exit = 2

    @property
    def is_local(self):
        return self == Kind.Local

    @property
    def is_entry(self):
        return self == Kind.Entry

    @property
    def is_exit(self):
        return self == Kind.Exit


LogItem = namedtuple("LogItem", "key val")


class Log(object):
    def __init__(self, timestamp: time = time.time(), items: List[LogItem] = None):
        self.timestamp = timestamp
        self.items = items or []

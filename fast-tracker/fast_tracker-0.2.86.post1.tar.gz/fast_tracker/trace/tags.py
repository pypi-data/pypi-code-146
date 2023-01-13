#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from collections import namedtuple

Tag = namedtuple("Tag", "key val overridable")
Tag.__new__.__defaults__ = (None, None, False)

# http
HttpUrl = "url"
HttpPath = "path"
HttpMethod = "http_method"
HttpStatus = "status_code"
HttpParams = "http_params"

# db
DbType = "db_type"
DbInstance = "db_instance"
DbStatement = "db_statement"
DbSqlParameters = "db_sql_parameters"

# mq
MqType = "mq_broker"
MqBroker = "mq_broker"
MqTopic = "mq_topic"
MqQueue = "mq_queue"

# cache
CacheType = "cache_type"
CacheInstance = "cache_instance"
CacheCommand = "cache_command"

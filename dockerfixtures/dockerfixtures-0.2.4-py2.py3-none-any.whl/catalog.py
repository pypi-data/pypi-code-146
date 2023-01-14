# -*- coding: utf-8; -*-
"""Provides a catalog of pre-defined docker images.
"""
from .image import Image


BUSYBOX_1_31_1_GLIBC = Image('busybox', tag='1.31.1-glibc')

__CONFLUENT_KAFKA_ENV = {
    'KAFKA_ADVERTISED_LISTENERS': ('LISTENERS_DOCKER_INTERNAL://${DOCKER_HOST_NAME}:9092,'
                                   'LISTENERS_DOCKER_EXTERNAL://${DOCKER_HOST_IP:-locahost}:9092'),
    'KAFKA_LISTENER_SECURITY_PROTOCOL_MAP': ('LISTENER_DOCKER_INTERNAL:PLAINTEXT,'
                                             'LISTENER_DOCKER_EXTERNAL:PLAINTEXT'),
    'KAFKA_BROKER_ID': '1',
}
CONFLUENT_KAFKA_5_0_0 = Image('confluentinc/kafka', tag='5.0.0', environment=__CONFLUENT_KAFKA_ENV)

__NCANIART_ALL_IN_ONE_KAFKA_ENV = {'ADVERTISED_HOST': '127.0.0.1',
                                   'KAFKA_HEAP_OPTS': '-Xmx256M -Xms256M',
                                   'ZOOKEEPER_HEAP_OPTS': '-Xmx128M -Xms128M',
                                   }
NCANIART_ALL_IN_ONE_KAFKA_LATEST = Image('ncaniart/all-in-one-kafka',
                                         tag='latest',
                                         environment=__NCANIART_ALL_IN_ONE_KAFKA_ENV)
NCANIART_ALL_IN_ONE_KAFKA_2_3_1 = Image('ncaniart/all-in-one-kafka',
                                        tag='2.3.1',
                                        environment=__NCANIART_ALL_IN_ONE_KAFKA_ENV)
NCANIART_ALL_IN_ONE_KAFKA_2_3_1_ALPINE = Image('ncaniart/all-in-one-kafka',
                                               tag='2.3.1-alpine',
                                               environment=__NCANIART_ALL_IN_ONE_KAFKA_ENV)

__PAPERLIB_KAFKA_ENV = {'ADVERTISED_HOST': '127.0.0.1',
                        'KAFKA_HEAP_OPTS': '-Xmx256M -Xms256M',
                        'ZOOKEEPER_HEAP_OPTS': '-Xmx128M -Xms128M',
                        }
PAPERLIB_KAFKA_LATEST = Image('paperlib/kafka',
                              environment=__PAPERLIB_KAFKA_ENV,
                              max_wait=20,
                              tag='latest')
PAPERLIB_KAFKA_2_3_1 = Image('paperlib/kafka',
                             environment=__PAPERLIB_KAFKA_ENV,
                             max_wait=20,
                             tag='2.3.1')
PAPERLIB_KAFKA_2_3_1_ALPINE = Image('paperlib/kafka',
                                    environment=__PAPERLIB_KAFKA_ENV,
                                    max_wait=20,
                                    tag='2.3.1-alpine')

__PG_ENV = {'PGDATA': None,
            'POSTGRES_DB': 'postgres',
            'POSTGRES_INITDB_ARGS': None,
            'POSTGRES_INITDB_WALDIR': None,
            # 'POSTGRES_PASSWORD': '',  # Warning: must be set for the container to start
            'POSTGRES_USER': 'postgres',
            }
PG_10 = Image('postgres', tag='10', environment=__PG_ENV)
PG_10_ALPINE = Image('postgres', tag='10-alpine', environment=__PG_ENV)
PG_11 = Image('postgres', tag='11', environment=__PG_ENV)
PG_11_ALPINE = Image('postgres', tag='11-alpine', environment=__PG_ENV)
PG_12 = Image('postgres', tag='12', environment=__PG_ENV)
PG_12_ALPINE = Image('postgres', tag='12-alpine', environment=__PG_ENV)
PG_96 = Image('postgres', tag='9.6', environment=__PG_ENV)
PG_96_ALPINE = Image('postgres', tag='9.6-alpine', environment=__PG_ENV)


# vim: et:sw=4:syntax=python:ts=4:

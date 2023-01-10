# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
triton client factory
"""
from .constants import RetryPolicy, ServiceConfig, GRPC_SERVICE, MethodConfigItem, NameItem
from .grpc_aio_client import TritonAioGRPCClient
from .http_aio_client import TritonAioHTTPClient
from .grpc_client import TritonGRPCClient
from .http_client import TritonHTTPClient


def _build_grpc_retry_channel_args(num_retries, max_interval_secs, base_interval_secs):
    channel_args = []
    retry_policy = RetryPolicy(
        maxAttempts=num_retries + 1,
        initialBackoff=f"{base_interval_secs}s",
        maxBackoff=f"{max_interval_secs}s",
        backoffMultiplier=2,
        retryableStatusCodes=["UNAVAILABLE",
                              "DEADLINE_EXCEEDED",
                              "UNKNOWN",
                              "ABORTED",
                              "INTERNAL",
                              "OUT_OF_RANGE"]
    )

    service_config = ServiceConfig(
        methodConfig=[MethodConfigItem(
            name=[NameItem(service=GRPC_SERVICE)],
            retryPolicy=retry_policy
        )]
    )
    channel_args.append(("grpc.service_config", service_config.json()))
    return channel_args


class TritonClientFactory:
    """
    Base client creator class that declares
    a factory method
    """

    @staticmethod
    def create_grpc_client(server_url,
                           num_retries=3,
                           max_interval_secs=20,
                           base_interval_secs=0.3,
                           verbose=False,
                           ssl=None,
                           authority="",
                           root_certificates="",
                           private_key="",
                           certificate_chain="",
                           creds=None,
                           keepalive_options=None
                           ):
        channel_args = _build_grpc_retry_channel_args(num_retries, max_interval_secs, base_interval_secs)
        return TritonGRPCClient(server_url=server_url,
                                verbose=verbose,
                                channel_args=channel_args,
                                ssl=ssl,
                                authority=authority,
                                root_certificates=root_certificates,
                                private_key=private_key,
                                certificate_chain=certificate_chain,
                                creds=creds,
                                keepalive_options=keepalive_options)

    @staticmethod
    def create_grpc_aio_client(server_url,
                               num_retries=3,
                               max_interval_secs=20,
                               base_interval_secs=0.3,
                               verbose=False,
                               ssl=None,
                               authority="",
                               root_certificates="",
                               private_key="",
                               certificate_chain="",
                               creds=None,
                               keepalive_options=None):
        channel_args = _build_grpc_retry_channel_args(num_retries, max_interval_secs, base_interval_secs)
        return TritonAioGRPCClient(server_url=server_url,
                                verbose=verbose,
                                channel_args=channel_args,
                                ssl=ssl,
                                authority=authority,
                                root_certificates=root_certificates,
                                private_key=private_key,
                                certificate_chain=certificate_chain,
                                creds=creds,
                                keepalive_options=keepalive_options)

    @staticmethod
    def create_http_client(
            server_url,
            verbose=False,
            concurrency=1,
            connection_timeout=60.0,
            network_timeout=60.0,
            max_greenlets=None,
            ssl=False,
            ssl_options=None,
            ssl_context_factory=None,
            insecure=False):
        """
        Parameters
        :param server_url:
        :param verbose:
        :param concurrency:
        :param connection_timeout:
        :param network_timeout:
        :param max_greenlets:
        :param ssl:
        :param ssl_options:
        :param ssl_context_factory:
        :param insecure:
        :return:
        """
        return TritonHTTPClient(server_url=server_url,
                                verbose=verbose,
                                concurrency=concurrency,
                                connection_timeout=connection_timeout,
                                network_timeout=network_timeout,
                                max_greenlets=max_greenlets,
                                ssl=ssl,
                                ssl_options=ssl_options,
                                ssl_context_factory=ssl_context_factory,
                                insecure=insecure)

    @staticmethod
    def create_http_aio_client(
            server_url,
            verbose=False,
            conn_limit=100,
            conn_timeout=60.0,
            ssl=False,
            ssl_context=None):
        """
        Parameters
        :param server_url:
        :param verbose:
        :param conn_limit:
        :param conn_timeout:
        :param ssl:
        :param ssl_context:
        :return:
        """
        return TritonAioHTTPClient(server_url=server_url,
                                verbose=verbose,
                                conn_limit=conn_limit,
                                conn_timeout=conn_timeout,
                                ssl=ssl,
                                ssl_context=ssl_context)

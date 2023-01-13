#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
from typing import Optional

import boto3
from botocore.config import Config
from minio import Minio


class Filemanager:
    """
    Simple Storage Service client to perform bucket and object
    operations for the Katonic File Manager.

    Args:
        access_key: Access key  of your File Manager inside your Katonic service account.
        secret_key: Secret Key of your File Manager inside your Katonic service account.

    Return:
        :class:`filemanager <Filemanger>` object

    Example::

        # Create client with access and secret key.
        client = Filemanager("ACCESS-KEY", "SECRET-KEY")
        # Create client with access key and secret key with specific region.
        client = Filemanager(
            access_key="Q3AM3UQ867SPQQA43P2F",
            secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
            region="us-east-2"
        )
    """

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        region: str = "us-east-1",
        read_timeout: int = 60,
        connect_timeout: int = 60,
        max_attempts: int = 5,
        retry_mode: str = "legacy"
    ):
        config = Config(
            signature_version="s3v4",
            read_timeout=read_timeout,
            connect_timeout=connect_timeout,
            retries={
                'max_attempts': max_attempts,
                'mode': retry_mode
            }
        )

        self.clientV1 = Minio(
            endpoint="minio-server.default.svc.cluster.local:9000",
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )

        self.resource = boto3.resource(
            "s3",
            endpoint_url="http://minio-server.default.svc.cluster.local:9000",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=config,
            region_name=region,
        )

        self.clientV2 = boto3.client(
            "s3",
            endpoint_url="http://minio-server.default.svc.cluster.local:9000",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=config,
            region_name=region,
        )

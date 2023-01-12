from datetime import datetime
from time import time

import botocore
from boto3 import Session
from boto3.s3.transfer import TransferConfig
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session
from dateutil.tz import tzlocal

from cnvrgv2.data.clients.base_storage_client import BaseStorageClient
from cnvrgv2.utils.retry import retry
from cnvrgv2.utils.storage_utils import create_dir_if_not_exists

config = TransferConfig(max_concurrency=10, use_threads=True)


class S3Storage(BaseStorageClient):
    def __init__(self, refresh_function):
        storage_meta = refresh_function()
        super().__init__(storage_meta)

        props = self._decrypt_dict(storage_meta, keys=["bucket", "region"])

        # An integer number to set the TTL for each session. Beyond this session, it will renew the token.
        # 30 minutes by default which is before the default role expiration of 1 hour
        self.session_ttl = 1800
        self.refresh_function = refresh_function
        self.bucket = props.get("bucket")
        self.region = props.get("region")
        self.client = self._get_client()

    @retry(log_error=True)
    def upload_single_file(self, local_path, object_path, progress_bar=None):
        try:
            self.client.upload_file(
                local_path,
                self.bucket,
                object_path,
                Config=config,
                Callback=self.progress_callback(progress_bar)
            )
        except Exception as e:
            print(e)

    @retry(log_error=True)
    def download_single_file(self, local_path, object_path, progress_bar=None):
        try:
            create_dir_if_not_exists(local_path)
            if not object_path:
                return

            self.client.download_file(
                self.bucket,
                object_path,
                local_path,
                Config=config,
                Callback=self.progress_callback(progress_bar)
            )
        except Exception as e:
            raise e

    def _refresh(self):

        props = self._decrypt_dict(self.refresh_function(), keys=["sts_a", "sts_s", "sts_st", "bucket", "region"])
        credentials = {
            "access_key": props.get("sts_a"),
            "secret_key": props.get("sts_s"),
            "token": props.get("sts_st"),
            "expiry_time": datetime.fromtimestamp(time() + self.session_ttl, tz=tzlocal()).isoformat()
        }
        return credentials

    def _get_client(self):
        session_credentials = RefreshableCredentials.create_from_metadata(
            metadata=self._refresh(),
            refresh_using=self._refresh,
            method="sts_assume_role"
        )
        session = get_session()
        session._credentials = session_credentials
        session.set_config_variable("region", self.region)
        autorefresh_session = Session(botocore_session=session)

        botocore_config = botocore.config.Config(max_pool_connections=50)
        return autorefresh_session.client('s3', config=botocore_config, verify=self.check_certificate)

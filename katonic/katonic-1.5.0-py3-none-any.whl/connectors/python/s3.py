#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
from pathlib import Path
from time import gmtime
from time import strftime
from typing import Optional

import boto3
import botocore.exceptions
from boto3 import Session
from colorama import Fore
from colorama import Style


class AWSS3Connector:
    """Provides AWS S3 Connector to extracts data from S3 Bucket."""

    _session: Optional[Session] = None

    def __init__(
        self,
        aws_access_key=None,
        aws_secret_key=None,
        aws_session_token=None,
        region_name=None,
        profile_name=None,
        bucket_name=None,
        object_name=None,
        file_name=None,
        output: str = "local",
        file_path=None,
    ):
        """
        Connect with AWS S3, fetch data from s3 and store into your output path.

        Args:
            aws_access_key (str): AWS access key ID to authenticate requests signed with an account key
            aws_secret_key (str): AWS secret access key
            bucket_name (str): AWS S3 bucket name
            aws_session_token (str): AWS temporary session token
            region_name (str): Default region when creating new connections
            profile_name (str): The name of a profile to use. If not given, then the default profile is used
            object_name (str): Name for the file to be downloaded. You can also give a name that is different from the object name.
                for e.g. If your file is existing as a.txt, you can download it as b.txt using this parameter
            file_name (str): Full path of your S3 Objects. Including the sub folders in your s3 Bucket. for e.g. /folder1/folder2/filename.txt
            output (str): output type, it can be `local` or `katonic` (default: `local` if not provided)
            file_path (str): output path where you want to store data

        Returns:
            None
        """
        self._aws_access_key = aws_access_key
        self._aws_secret_key = aws_secret_key
        self._bucket_name = bucket_name
        self._aws_session_token = aws_session_token
        self._region_name = region_name
        self._profile_name = profile_name
        self._object_name = object_name
        self._file_name = file_name
        self._output = output
        self._file_path = file_path

        if self._output.lower() == "local":
            Path(self._file_path).mkdir(
                parents=True, exist_ok=True
            ) if self._file_path else ""
            self._dst_path = (
                Path(self._file_path).absolute()
                if self._file_path
                else Path().absolute()
            )
        elif self._output.lower() == "katonic":
            if self._file_path:
                Path(f"/kfs_private/{self._file_path}").mkdir(
                    parents=True, exist_ok=True
                )
                self._dst_path = Path(f"/kfs_private/{self._file_path}").absolute()
            else:
                self._dst_path = Path("/kfs_private/").absolute()
        else:
            raise ValueError(
                f"invalid literal for variable output: '{self._output}', it must be one from 'local' or 'katonic'."
            )

    def _get_boto_reg_conn(self):
        """Creates a session to the aws."""

        if not self._session:
            self._session = boto3.Session(
                aws_access_key_id=self._aws_access_key,
                aws_secret_access_key=self._aws_secret_key,
                aws_session_token=self._aws_session_token,
                region_name=self._region_name,
                profile_name=self._profile_name,
            )

        return self._session

    def get_data(self) -> None:  # checked
        """
        This function will extracts data from AWS S3.

        Returns:
            None

        Raises:
            ValueError: if output type provided other than `local` or `katonic`.
        """
        _obj_name, ext = self._object_name.split(".")
        fname = f"s3_{self._file_name or _obj_name.split('/')[-1]}_{strftime('%Y_%m_%d_%H_%M_%S', gmtime())}.{ext}"

        self._dstn_path = f"{self._dst_path}/{fname}"
        try:
            _session = self._get_boto_reg_conn()
            s3 = _session.resource("s3")
            print("Connection instance to aws s3 stablished Successfully.")
        except botocore.exceptions.ClientError as e:
            raise e
        except botocore.exceptions.ParamValidationError as e:
            raise ValueError(f"The parameters you provided are incorrect: {e}") from e
        else:
            try:
                s3.Bucket(self._bucket_name).download_file(
                    Key=self._object_name, Filename=self._dstn_path
                )

                print(
                    f"File saved to your {Style.BRIGHT + Fore.GREEN}'{self._output}'{Style.RESET_ALL}"
                    f"file system with name {Style.BRIGHT + Fore.GREEN}'{fname}'{Style.RESET_ALL} Successfully."
                )

            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    print("The object does not exist.")
                else:
                    raise e

# -*- coding: utf-8 -*-
""" Upload Image files to an S3 bucket """


import os
import boto3
import pprint
from typing import List
from boto3.resources.factory import ServiceResource

from baseblock import EnvIO
from baseblock import FileIO
from baseblock import Stopwatch
from baseblock import BaseObject

from awsfile_helper.dmo import S3BucketReader
from awsfile_helper.dmo import S3ImageWriter
from awsfile_helper.dmo import FileContentWriter


class UploadImageFiles(BaseObject):
    """ Upload Image files to an S3 bucket """

    def __init__(self,
                 s3_client: ServiceResource):
        """ Change Log

        Created:
            13-Jan-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/awsfile-helper/issues/5

        Args:
            s3 (ServiceResource): an activated s3 resource
        """
        BaseObject.__init__(self, __name__)
        self._s3_client = s3_client

    def process(self,
                bucket_name: str,
                folder_name: str,
                file_paths: List[str]) -> None:
        """ Open and Read S3 Files

        Args:
            bucket_name (str): the name of the S3 bucket
            folder_name (str): a folder that pre-exists within this S3 bucket
            file_paths (List[str]): a list of fully qualified file paths
        """

        for file_path in file_paths:
            with open(file_path, 'rb') as data:

                def get_file_name() -> str:
                    if folder_name.endswith('/'):
                        return f'{folder_name}{os.path.basename(file_path)}'
                    return f'{folder_name}/{os.path.basename(file_path)}'

                self._s3_client.upload_fileobj(
                    data, bucket_name, get_file_name())

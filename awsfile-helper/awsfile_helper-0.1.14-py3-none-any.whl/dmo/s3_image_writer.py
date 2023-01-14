# -*- coding: utf-8 -*-
""" Download an Image from S3 """


import boto3
import botocore

from boto3.resources.factory import ServiceResource

from baseblock import EnvIO
from baseblock import FileIO
from baseblock import BaseObject


class S3ImageWriter(BaseObject):
    """ Download an Image from S3 """

    def __init__(self,
                 s3: ServiceResource):
        """ Change Log

        Created:
            11-Oct-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/awsfile-helper/issues/1
        Updated:
            1-Nov-2022
            craigtrim@gmail.com
            *   retrieve local directory from environment
                https://github.com/craigtrim/awsfile-helper/issues/3
        """
        BaseObject.__init__(self, __name__)
        self._s3 = s3
        self._local_directory = FileIO.local_directory_by_name(
            EnvIO.str_or_default('LOCAL_DIRECTORY_NAME', 'AWSFileHelper'))

    def process(self,
                bucket_name: str,
                file_name: str) -> str or None:
        """ Open and Read S3 Files

        Args:
            bucket_name (str): the name of the S3 bucket
            file_name (str): the file name (or prefix) to search for

        Returns:
            str: the file path of the image
        """

        file_path = FileIO.join(self._local_directory, file_name)

        if FileIO.exists(file_path):
            return file_path

        s3 = boto3.resource('s3')

        try:
            s3.Bucket(bucket_name).download_file(file_name, file_path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                self.logger.error('The object does not exist.')
            else:
                raise

        return file_path

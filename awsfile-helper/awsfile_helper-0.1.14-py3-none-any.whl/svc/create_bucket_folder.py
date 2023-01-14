# -*- coding: utf-8 -*-
""" Read files from an S3 Bucket and persist locally """


import os
import boto3
import pprint
from boto3.resources.factory import ServiceResource

from baseblock import EnvIO
from baseblock import FileIO
from baseblock import Stopwatch
from baseblock import BaseObject

from awsfile_helper.dmo import S3BucketReader
from awsfile_helper.dmo import S3ImageWriter
from awsfile_helper.dmo import FileContentWriter


class CreateBucketFolder(BaseObject):
    """ Read files from an S3 Bucket and persist locally """

    def __init__(self,
                 s3: ServiceResource):
        """ Change Log

        Created:
            13-Jan-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/awsfile-helper/issues/5

        Args:
            s3 (ServiceResource): an activated s3 resource
        """
        BaseObject.__init__(self, __name__)
        self._s3 = s3

    def process(self,
                bucket_name: str,
                folder_name: str) -> None:
        """ Open and Read S3 Files

        Args:
            bucket_name (str): the name of the S3 bucket
            folder_name (str): the name of the folder in the S3 bucket
        """

        sw = Stopwatch()

        self._s3.put_object(Bucket=bucket_name, Key=(folder_name + '/'))

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                'S3 Bucket Creation Completed',
                f'\tBucket Name: {bucket_name}',
                f'\tTotal Time: {str(sw)}']))

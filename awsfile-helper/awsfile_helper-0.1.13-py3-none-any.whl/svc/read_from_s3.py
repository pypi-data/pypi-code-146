# -*- coding: utf-8 -*-
""" Read from an S3 Bucket """


from boto3.resources.factory import ServiceResource

from baseblock import Stopwatch
from baseblock import BaseObject

from awsfile_helper.dmo import S3BucketReader


class ReadFromS3(BaseObject):
    """ Read from an S3 Bucket """

    def __init__(self,
                 s3: ServiceResource):
        """ Change Log

        Created:
            22-Jul-2022
            craigtrim@gmail.com
            *   https://bast-ai.atlassian.net/browse/COR-8
        Updated:
            25-Jul-2022
            craigtrim@gmail.com
            *   integrate 'write-to-temp' capability
                https://bast-ai.atlassian.net/browse/COR-11
        """
        BaseObject.__init__(self, __name__)
        self._read = S3BucketReader(s3).process

    def process(self,
                bucket_name: str,
                file_name: str,
                load_files: bool) -> dict:
        """ Open and Read S3 Files

        Args:
            bucket_name (str): the name of the S3 bucket
            file_name (str): the file name (or prefix) to search for
            load_files (bool): load the contents of the input files
                if None, the keyed value will be None

        Returns:
            dict: a dictionary of file contents keyed by file name
        """

        sw = Stopwatch()

        d_results = self._read(bucket_name=bucket_name,
                               file_name=file_name,
                               load_files=load_files)

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                'S3 Bucket Read Completed',
                f'\tBucket Name: {bucket_name}',
                f'\tFile Name: {file_name}',
                f'\tTotal Time: {str(sw)}',
                f'\tTotal Files: {len(d_results)}']))

        return d_results

# -*- coding: utf-8 -*-
""" Read files from an S3 Bucket and persist locally """


import os
from boto3.resources.factory import ServiceResource

from baseblock import EnvIO
from baseblock import FileIO
from baseblock import Stopwatch
from baseblock import BaseObject

from awsfile_helper.dmo import S3BucketReader
from awsfile_helper.dmo import S3ImageWriter
from awsfile_helper.dmo import FileContentWriter


class DownloadFromS3(BaseObject):
    """ Read files from an S3 Bucket and persist locally """

    def __init__(self,
                 s3: ServiceResource):
        """ Change Log

        Created:
            25-Jul-2022
            craigtrim@gmail.com
            *   integrate 'write-to-temp' capability
                https://bast-ai.atlassian.net/browse/COR-11
        Created:
            5-Aug-2022
            craigtrim@gmail.com
            *   make the logging around cache retrieval obvious, in pursuit of
                https://bast-ai.atlassian.net/browse/COR-59
        Created:
            6-Aug-2022
            craigtrim@gmail.com
            *   renamed from 'persist-from-s3'
            *   remove code caching; this has bewen refactored into 'read-from-cache'
                https://bast-ai.atlassian.net/browse/COR-72
        Created:
            11-Oct-2022
            craigtrim@gmail.com
            *   integrate s3-image-writer
                https://github.com/craigtrim/awsfile-helper/issues/1
        Updated:
            1-Nov-2022
            craigtrim@gmail.com
            *   retrieve local directory from environment
                https://github.com/craigtrim/awsfile-helper/issues/3
        """
        BaseObject.__init__(self, __name__)
        self._local_directory = FileIO.local_directory_by_name(
            EnvIO.str_or_default('LOCAL_DIRECTORY_NAME', 'AWSFileHelper'))

        self._read = S3BucketReader(s3).process
        self._download_image = S3ImageWriter(s3).process
        self._write_to_disk = FileContentWriter().process

    def _construct_local_path(self,
                              file_path: str) -> str:
        if file_path:
            FileIO.exists_or_create(file_path)
            return file_path
        return self._local_directory

    def _process(self,
                 bucket_name: str,
                 file_name: str,
                 file_path: str = None,
                 load_files: bool = True) -> dict:

        d_paths = {}
        basename = os.path.basename(file_name)

        file_ext = basename.split('.')[-1].strip()
        if file_ext in ['jpg', 'png']:
            local_path = self._download_image(
                bucket_name=bucket_name,
                file_name=file_name)
            d_paths[basename] = local_path

            return d_paths

        d_files = self._read(bucket_name=bucket_name,
                             file_name=file_name,
                             load_files=load_files)

        for k in d_files:

            local_path = os.path.normpath(
                os.path.join(self._construct_local_path(file_path), k))

            path_only = os.path.sep.join(local_path.split(os.path.sep)[:-1])
            FileIO.exists_or_create(path_only)

            self._write_to_disk(file_data=d_files[k],
                                file_path=local_path,
                                file_ext=file_ext)

            d_paths[k] = local_path

        return d_paths

    def process(self,
                bucket_name: str,
                file_name: str,
                file_path: str = None) -> dict:
        """ Open and Read S3 Files

        Args:
            bucket_name (str): the name of the S3 bucket
            file_name (str): the file name (or prefix) to search for
            file_path (str, optional): the path to persist the files. Defaults to None.
                if the file path is left blank, the system will use the local app data or temp directory
                appropriate to the platform hosting this service

        Returns:
            dict: a dictionary of file paths keyed by file name
        """

        sw = Stopwatch()

        d_paths = self._process(
            bucket_name=bucket_name,
            file_name=file_name,
            file_path=file_path)

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                'S3 Bucket Read Completed',
                f'\tBucket Name: {bucket_name}',
                f'\tFile Name: {file_name}',
                f'\tTotal Time: {str(sw)}',
                f'\tTotal Files: {len(d_paths)}']))

        return d_paths

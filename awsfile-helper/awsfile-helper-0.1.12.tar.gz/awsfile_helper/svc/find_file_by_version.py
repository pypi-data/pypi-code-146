# -*- coding: utf-8 -*-
""" Find the Latest Version number of a File """


from typing import Callable

from baseblock import BaseObject


class FindFileByVersion(BaseObject):
    """ Find the Latest Version number of a File """

    def __init__(self,
                 download_files: Callable):
        """ Change Log

        Created:
            29-Jul-2022
            craigtrim@gmail.com
            *   https://bast-ai.atlassian.net/browse/COR-28?focusedCommentId=10070
        """
        BaseObject.__init__(self, __name__)
        self._download_files = download_files

    def process(self,
                bucket_name: str,
                file_name: str,
                file_ext: str,
                version: str) -> str:
        """ Download a versioned Bast S3 file to a local directory

        Args:
            bucket_name (str): the name of the bucket
                e.g., name-of-bucket
            file_name (str): the qualified name of the file
                e.g., 'training/myeliza/doctor'
            file_ext (str): the file extension
                e.g., 'txt'
            version (str): the version of the file to access
                e.g., '0.1.0'

        Returns:
            str: the local path of the downloaded S3 file
        """

        def logical_name() -> str:
            return file_name.split('/')[-1].strip()

        basename = f'{logical_name()}-{version}.{file_ext}'
        target_file = f'{file_name}/{version}/{basename}'

        d_paths = self._download_files(bucket_name=bucket_name,
                                       file_name=target_file)

        return d_paths[target_file]

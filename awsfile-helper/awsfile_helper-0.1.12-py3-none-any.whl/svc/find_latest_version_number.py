# -*- coding: utf-8 -*-
""" Find the Latest Version number of a File """


import os
from typing import Callable

from baseblock import BaseObject


class FindLatestVersionNumber(BaseObject):
    """ Find the Latest Version number of a File """

    def __init__(self,
                 read_files: Callable):
        """ Change Log

        Created:
            29-Jul-2022
            craigtrim@gmail.com
            *   https://bast-ai.atlassian.net/browse/COR-28?focusedCommentId=10070
        """
        BaseObject.__init__(self, __name__)
        self._read_files = read_files

    def process(self,
                bucket_name: str,
                file_name: str) -> str or None:
        """ Get the Latest Version of a File

        Args:
            bucket_name (str): the name of the bucket
                e.g., name-of-bucket
            file_name (str): the qualified name of the file
                e.g., 'training/myeliza/doctor'

        Returns:
            str or None: the latest version
                e.g., '0.1.2'
        """
        results = self._read_files(bucket_name=bucket_name,
                                   file_name=file_name,
                                   load_files=False)

        if not results or not len(results):
            return None

        results = [os.path.basename(x) for x in results]
        results = [x for x in results if x and len(x) and '.' in x]
        if not results or not len(results):
            return None

        results = ['.'.join(x.split('-')[-1].split('.')[:3]) for x in results]
        if not results or not len(results):
            return None

        def get_latest_version() -> str:
            if not len(results):
                return None
            if len(results) == 1:
                return results[0]
            return sorted(results)[-1]

        latest_version = get_latest_version()

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                'Retrieved Latest Version',
                f'\tBucket Name: {bucket_name}',
                f'\tFile Name: {file_name}',
                f'\tLatest Version: {latest_version}']))

        return latest_version

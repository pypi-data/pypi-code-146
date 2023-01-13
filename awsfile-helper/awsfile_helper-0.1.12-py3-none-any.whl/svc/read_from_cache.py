# -*- coding: utf-8 -*-
""" Avoid and S3 call and Read File direct from Cache """


import os

from baseblock import EnvIO
from baseblock import FileIO
from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject


class ReadFromCache(BaseObject):
    """ Avoid and S3 call and Read File direct from Cache """

    def __init__(self):
        """ Change Log

        Created:
            6-Aug-2022
            craigtrim@gmail.com
            *   https://bast-ai.atlassian.net/browse/COR-72
        Updated:
            1-Nov-2022
            craigtrim@gmail.com
            *   retrieve local directory from environment
                https://github.com/craigtrim/awsfile-helper/issues/3
        """
        BaseObject.__init__(self, __name__)
        self._local_directory = FileIO.local_directory_by_name(
            EnvIO.str_or_default('LOCAL_DIRECTORY_NAME', 'AWSFileHelper'))

    def process(self,
                file_name: str,
                file_ext: str,
                file_version: str) -> dict or None:
        sw = Stopwatch()

        if self.isEnabledForDebug:
            Enforcer.is_str(file_name)
            Enforcer.is_str(file_ext)
            Enforcer.is_str(file_version)

        file_name = FileIO.normpath(file_name)
        file_path = file_name
        file_name = f"{file_name.split('/')[-1]}-{file_version}.{file_ext}"

        cached_copy = FileIO.join(self._local_directory,
                                  file_path,
                                  file_version,
                                  file_name)

        if FileIO.exists(cached_copy):

            if self.isEnabledForDebug:
                self.logger.debug('\n'.join([
                    'Cached Read Completed',
                    f'\tLocal Directory: {self._local_directory}',
                    f'\tFile Name: {file_name}',
                    f'\tTotal Time: {str(sw)}',
                    '\tTotal Files: 1']))

            return cached_copy

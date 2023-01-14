# -*- coding: utf-8 -*-
""" Find Cloud files on S3 within the a given bucket """


import os
from typing import Optional

from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject

from awsfile_helper import AwsAPI
from awsfile_helper import ReadFromCache
from awsfile_helper import FileContentReader


class FindS3File(BaseObject):
    """ Find Cloud files on S3 within the a given bucket """

    __awsapi = None

    def __init__(self,
                 bucket_name: str,
                 file_name: str,
                 file_ext: str,
                 file_version: Optional[str] = None,
                 aws_access_key: Optional[str] = None,
                 aws_secret_key: Optional[str] = None):
        """ Change Log

        Created:
            26-Jul-2022
            craigtrim@gmail.com
            *   https://bast-ai.atlassian.net/browse/COR-17
        Updated:
            4-Aug-2022
            craigtrim@gmail.com
            *   migrated out of 'oureliza' into a 'awsfile_helper/recipe'
                https://bast-ai.atlassian.net/browse/COR-50
        Updated:
            5-Aug-2022
            craigtrim@gmail.com
            *   adhere to latest standard on file version
                https://bast-ai.atlassian.net/browse/COR-59
        Updated:
            1-Nov-2022
            craigtrim@gmail.com
            *   remove hard-coded bucket names
                https://github.com/craigtrim/awsfile-helper/issues/2
        Updated:
            11-Nov-2022
            craigtrim@gmail.com
            *   pass keys as parameters
                https://github.com/craigtrim/awsfile-helper/issues/4

        Args:
            bucket_name (str): the name of the bucket
            file_name (str): the qualified name of the file to retrieve
            file_ext (str): the file's extension
            file_version (str, optional): the file version. Defaults to '*'.
                the default '*' will always retrieve the latest version
            aws_access_key (str, Optional): Encrypted AWS Access Key
                if the key is not provided as a parameter,
                it must be encrypted within the environment as AWS_ACCESS_KEY
            aws_secret_key (str, Optional): Encrypted AWS Secret Key
                if the key is not provided as a parameter,
                it must be encrypted within the environment as AWS_SECRET_KEY
        """
        BaseObject.__init__(self, __name__)
        if self.isEnabledForDebug:
            Enforcer.is_str(bucket_name)
            Enforcer.is_str(file_name)
            Enforcer.is_str(file_ext)
            Enforcer.is_optional_str(file_version)
            Enforcer.is_optional_str(aws_access_key)
            Enforcer.is_optional_str(aws_secret_key)

        self._bucket_name = bucket_name
        self._file_name = file_name
        self._file_ext = file_ext
        self._file_version = file_version
        self._access_key = aws_access_key
        self._secret_key = aws_secret_key
        self._read_contents = FileContentReader().process

    def _awsapi(self) -> AwsAPI:
        """ Lazy Loading to avoid any S3 Connections until required

        Returns:
            AwsAPI: an instantiated API
        """
        if not self.__awsapi:
            self.__awsapi = AwsAPI(
                aws_access_key=self._access_key,
                aws_secret_key=self._secret_key)
        return self.__awsapi

    def _resolve_file_version(self) -> str:
        """ Resolve Wildcard Versions

        Returns:
            str: the version to use
        """
        if not self._file_version or not len(self._file_version):

            # e.g., 'training/intents/chitchat' => 'TRAINING_INTENTS_CHITCHAT_VERSION'
            key = f"{self._file_name.replace('/', '_').upper()}_VERSION"
            if key in os.environ:
                self._file_version = os.environ[key]

            else:
                self._file_version = '*'

        if self._file_version == '*':
            self._file_version = self._awsapi().latest_version_number(
                bucket_name=self._bucket_name,
                file_name=self._file_name)

        return self._file_version

    def _read_from_cache(self,
                         sw: Stopwatch,
                         file_version: str) -> dict or None:

        cached_file_path = ReadFromCache().process(
            file_name=self._file_name,
            file_ext=self._file_ext,
            file_version=file_version)

        if cached_file_path:
            contents = self._read_contents(file_path=cached_file_path,
                                           file_ext=self._file_ext)

            if self.isEnabledForDebug:
                self.logger.debug('\n'.join([
                    'Retrieved Cached File',
                    f'\tTotal Time: {str(sw)}',
                    f'\tFile Version: {file_version}',
                    f'\tCached Path: {cached_file_path}']))

            return {
                'path': cached_file_path,
                'version': file_version,
                'contents': contents
            }

    def _read_from_s3(self,
                      sw: Stopwatch,
                      file_version: str) -> dict:

        # access the training file from S3
        local_file_path = self._awsapi().file_by_version(
            bucket_name=self._bucket_name,
            file_name=self._file_name,
            file_ext=self._file_ext,
            version=file_version)

        contents = self._read_contents(file_path=local_file_path,
                                       file_ext=self._file_ext)

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                'Retrieved Cloud File',
                f'\tTotal Time: {str(sw)}',
                f'\tBucket Name: {self._bucket_name}',
                f'\tFile Version: {file_version}',
                f'\tLocal Path: {local_file_path}']))

        return {
            'path': local_file_path,
            'version': file_version,
            'contents': contents
        }

    def process(self) -> dict:
        """ Retrieve the S3 File

        Raises:
            NotImplementedError: the extension is not recognized

        Returns:
            dict: the file contents, path and version
        """

        sw = Stopwatch()

        # if we have a specific version
        if self._file_version and self._file_version != '*':

            # try to find this file in the cache
            d_result = self._read_from_cache(sw, self._file_version)

            if d_result:  # we found it; early exit
                return d_result

        # no specific version given; find the latest on S3
        resolved_version = self._resolve_file_version()

        # now check the cache and see if this version exists
        d_result = self._read_from_cache(sw, resolved_version)

        if d_result:  # we found it ...
            return d_result

        # file is not yet on disk; retrieve from S3
        return self._read_from_s3(sw, resolved_version)

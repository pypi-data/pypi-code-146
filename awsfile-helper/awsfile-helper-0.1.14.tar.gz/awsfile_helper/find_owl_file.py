# -*- coding: utf-8 -*-
""" Find Ontology files on S3 within a given bucket """


import os
from typing import Optional

from baseblock import Enforcer
from baseblock import BaseObject


class FindOwlFile(BaseObject):
    """ Find Ontology files on S3 within a given bucket """

    def __init__(self,
                 bucket_name: str,
                 file_name: str,
                 file_version: Optional[str] = None,
                 aws_access_key: Optional[str] = None,
                 aws_secret_key: Optional[str] = None):
        """ Change Log

        Created:
            6-Aug-2022
            craigtrim@gmail.com
            *   refactored out of 'ontology-by-version' in pursuit of
                https://bast-ai.atlassian.net/browse/COR-74
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
            file_version (str, optional): the file version. Defaults to '*'.
                the default '*' will always retrieve the latest version
        """
        BaseObject.__init__(self, __name__)
        if self.isEnabledForDebug:
            Enforcer.is_str(bucket_name)
            Enforcer.is_str(file_name)
            Enforcer.is_optional_str(file_version)
            Enforcer.is_optional_str(aws_access_key)
            Enforcer.is_optional_str(aws_secret_key)

        if not file_name.startswith('ontologies/'):
            file_name = f'ontologies/{file_name}'

        self._file_name = file_name
        self._bucket_name = bucket_name
        self._file_version = file_version
        self._access_key = aws_access_key
        self._secret_key = aws_secret_key

    def process(self) -> dict:

        from awsfile_helper import FindS3File

        d_owl_file = FindS3File(
            file_ext='owl',
            file_name=self._file_name,
            bucket_name=self._bucket_name,
            file_version=self._file_version,
            aws_access_key=self._access_key,
            aws_secret_key=self._secret_key).process()

        d_txt_file = FindS3File(
            file_ext='txt',
            file_name=self._file_name,
            bucket_name=self._bucket_name,
            file_version=d_owl_file['version'],
            aws_access_key=self._access_key,
            aws_secret_key=self._secret_key).process()

        return {
            'owl': d_owl_file,
            'txt': d_txt_file,
            'path': os.path.dirname(d_owl_file['path'])
        }

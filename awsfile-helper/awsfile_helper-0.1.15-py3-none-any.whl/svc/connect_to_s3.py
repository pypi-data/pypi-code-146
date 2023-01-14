# -*- coding: utf-8 -*-
""" Connect to S3 """


from typing import Optional

from boto3 import client
from boto3 import resource
from boto3.resources.factory import ServiceResource

from baseblock import BaseObject

from awsfile_helper.dmo import CredentialManager


class ConnectToS3(BaseObject):
    """ Connect to S3 """

    def __init__(self,
                 aws_access_key: Optional[str] = None,
                 aws_secret_key: Optional[str] = None):
        """ Change Log

        Created:
            22-Jul-2022
            craigtrim@gmail.com
            *   https://bast-ai.atlassian.net/browse/COR-8
        Updated:
            11-Nov-2022
            craigtrim@gmail.com
            *   pass keys as parameters
                https://github.com/craigtrim/awsfile-helper/issues/4
        Updated:
            13-Jan-2023
            craigtrim@gmail.com
            *   add resource and client functions (deprecate process(...))
                https://github.com/craigtrim/awsfile-helper/issues/6
            *   add rekognition and textract functions
                https://github.com/craigtrim/awsfile-helper/issues/7

        Args:
            aws_access_key (str, Optional): Encrypted AWS Access Key
                if the key is not provided as a parameter,
                it must be encrypted within the environment as AWS_ACCESS_KEY
            aws_secret_key (str, Optional): Encrypted AWS Secret Key
                if the key is not provided as a parameter,
                it must be encrypted within the environment as AWS_SECRET_KEY
        """
        BaseObject.__init__(self, __name__)
        self._creds = CredentialManager(aws_access_key=aws_access_key,
                                        aws_secret_key=aws_secret_key)

    def process(self) -> ServiceResource:
        return self.resource()  # deprecated

    def resource(self) -> ServiceResource:
        s3 = resource('s3',
                      aws_access_key_id=self._creds.access_key(),
                      aws_secret_access_key=self._creds.secret_key())

        return s3

    def client(self) -> ServiceResource:
        s3 = client('s3',
                    aws_access_key_id=self._creds.access_key(),
                    aws_secret_access_key=self._creds.secret_key())

        return s3

    def rekognition(self) -> ServiceResource:
        return client('rekognition',
                      aws_access_key_id=self._creds.access_key(),
                      aws_secret_access_key=self._creds.secret_key())

    def textract(self) -> ServiceResource:
        return client('textract',
                      aws_access_key_id=self._creds.access_key(),
                      aws_secret_access_key=self._creds.secret_key())

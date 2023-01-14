# -*- coding: utf-8 -*-
""" Manage AWS Credentials """


from typing import Optional

from baseblock import EnvIO
from baseblock import CryptoBase
from baseblock import BaseObject


class CredentialManager(BaseObject):
    """ Manage AWS Credentials """

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

        Args:
            aws_access_key (str, Optional): Encrypted AWS Access Key
                if the key is not provided as a parameter,
                it must be encrypted within the environment as AWS_ACCESS_KEY
            aws_secret_key (str, Optional): Encrypted AWS Secret Key
                if the key is not provided as a parameter,
                it must be encrypted within the environment as AWS_SECRET_KEY
        """
        BaseObject.__init__(self, __name__)
        self._access_key = aws_access_key
        self._secret_key = aws_secret_key

    def access_key(self) -> str:
        """ AWS Access Key

        Returns:
            str: decrypted AWS access key
        """
        if self._access_key:
            return CryptoBase().decrypt_str(self._access_key)
        return CryptoBase().decrypt_str(EnvIO.str_or_exception('AWS_ACCESS_KEY'))

    def secret_key(self) -> str:
        """ AWS Secret Key

        Returns:
            str: decrypted AWS secret key
        """
        if self._secret_key:
            return CryptoBase().decrypt_str(self._secret_key)
        return CryptoBase().decrypt_str(EnvIO.str_or_exception('AWS_SECRET_KEY'))

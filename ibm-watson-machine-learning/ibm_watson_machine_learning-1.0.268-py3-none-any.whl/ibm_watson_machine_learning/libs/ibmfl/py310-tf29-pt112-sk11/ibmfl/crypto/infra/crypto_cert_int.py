#  (C) Copyright IBM Corp. 2022.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import abc
from ibmfl.crypto.crypto_exceptions import *

class CryptoCert:
    """
    This class defines an interface for certificate verification functions. 
    """

    @abc.abstractmethod
    def __init__(self, ca_cert_file_path: str, my_cert_file_path: str, **kwargs):
        return

    @abc.abstractmethod
    def verify_cert_signature(self, certificate):
        raise NotImplementedError

    def verify_certs(self, certificates):
        ret = {}
        for id, cert in certificates.items():
            ver, pbkey = self.verify_cert_signature(cert)
            if not ver:
                raise KeyDistributionVerificationException("Invalid certificate=" + repr(cert))
            ret[id] = pbkey
        return ret

    @abc.abstractmethod
    def get_my_cert(self, ret_type: str):
        raise NotImplementedError

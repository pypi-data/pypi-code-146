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

class CryptoSym(abc.ABC):
    """
    This class defines an interface for symmetric encryption functions. 
    """

    @abc.abstractmethod
    def __init__(self, key: bytes = None, **kwargs):
        self.key = key
        self.cipher = None
        return

    @abc.abstractmethod
    def generate_key(self):
        raise NotImplementedError

    def get_key(self) -> bytes:
        if self.key is None:
            raise KeyDistributionInputException("self.key is None")
        return self.key

    def encrypt(self, plain_data: bytes) -> bytes:
        if self.cipher is None:
            raise KeyDistributionInputException("self.cipher is None")
        return self.cipher.encrypt(plain_data)        

    def decrypt(self, cipher_data: bytes) -> bytes:
        if self.cipher is None:
            raise KeyDistributionInputException("self.cipher is None")
        return self.cipher.decrypt(cipher_data)

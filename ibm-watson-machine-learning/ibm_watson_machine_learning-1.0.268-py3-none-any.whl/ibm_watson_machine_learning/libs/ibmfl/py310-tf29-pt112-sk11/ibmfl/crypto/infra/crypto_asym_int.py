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

class CryptoAsym(abc.ABC):
    """
    This class defines an interface for asymmetric encryption functions. 
    """

    @abc.abstractmethod
    def __init__(self, key_file: str = None, password: bytes = None, **kwargs):
        return

    @abc.abstractstaticmethod
    def generate_key():
        raise NotImplementedError

    @abc.abstractmethod
    def get_public_key(self, type: str):
        raise NotImplementedError

    @abc.abstractmethod
    def write_key_file(self, file_path: str, password: bytes):
        raise NotImplementedError

    @abc.abstractmethod
    def encrypt(self, plain_data: bytes) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    def decrypt(self, cipher_data: bytes) -> bytes:
        raise NotImplementedError

    @abc.abstractstaticmethod
    def encrypt_wkey(public_key, plain_data: bytes) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    def get_signature(self, data: bytes) -> bytes:
        raise NotImplementedError

    @abc.abstractstaticmethod
    def verify_signature(public_key, signature: bytes, data: bytes) -> bool:
        raise NotImplementedError

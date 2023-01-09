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
from cryptography.fernet import Fernet
from ibmfl.crypto.infra.crypto_sym_int import CryptoSym


class CryptoSymFernet(CryptoSym):
    """
    This class implements the interface for symmetric encryption functions using Fernet.
    """

    def __init__(self, key: bytes = None, **kwargs):
        super(CryptoSymFernet, self).__init__(key)
        if key is None:
            self.generate_key()
        else:
            self.key = key
            self.cipher = Fernet(self.key)

    def generate_key(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        return

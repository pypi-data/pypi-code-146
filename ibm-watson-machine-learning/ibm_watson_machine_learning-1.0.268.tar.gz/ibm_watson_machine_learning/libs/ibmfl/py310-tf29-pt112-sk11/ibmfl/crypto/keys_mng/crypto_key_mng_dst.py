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
from ibmfl.crypto.keys_mng.crypto_key_mng_int import KeyManager
from ibmfl.crypto.crypto_exceptions import KeyManagerException

class DistributionKeyManager(KeyManager):

    def __init__(self, config):
        """ Initialize Key from local key file"""
        if config and 'distribution' not in config:
            raise KeyManagerException('keys distribution configuration is not provided')
        self.keys = config

    def initialize_keys(self, **kwargs):
        """ Initialize the keys directly from the config file"""
        return self.keys

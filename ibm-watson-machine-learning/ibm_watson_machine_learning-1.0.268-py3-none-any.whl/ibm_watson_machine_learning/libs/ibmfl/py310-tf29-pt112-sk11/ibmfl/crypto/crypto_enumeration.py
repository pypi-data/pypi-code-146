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
"""
 An enumeration class for the crypto type field which describe what
 kind of data is being sent inside the Message
"""
from enum import Enum


class CryptoEnum(Enum):
    """
    Crypto types used for secure aggregation
    """
    CRYPTO_PAILLIER = 'Paillier'
    CRYPTO_THRESHOLD_PAILLIER = 'ThresholdPaillier'
    CRYPTO_MIFE = 'MIFE'
    CRYPTO_MCFE = 'MCFE'
    CRYPTO_DECENTRALIZED_MIFE = 'DMIFE'
    CRYPTO_FHE = 'FHE'

    KEY_PUBLIC_PARAMETER = 'pp'
    KEY_PRIVATE = 'sk'
    KEY_DECTYPT = 'dk'
    WEIGHTS_PLAINTEXT = 'plaintext-weights'
    WEIGHTS_CIPHERTEXT = 'ciphertext-weights'

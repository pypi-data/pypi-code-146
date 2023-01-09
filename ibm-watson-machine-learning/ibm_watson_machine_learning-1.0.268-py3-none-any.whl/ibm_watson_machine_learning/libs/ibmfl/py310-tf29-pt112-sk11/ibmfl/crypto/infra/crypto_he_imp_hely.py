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
import importlib
if importlib.util.find_spec("pyhelayers") is not None:
    import pyhelayers as pyhe
from ibmfl.crypto.infra.crypto_he_int import CryptoHe
from ibmfl.crypto.crypto_exceptions import *

class CryptoHeLy(CryptoHe):
    """
    This class implements the interface for HE keys generation functions using pyhelayers. 
    """

    CONFIG_FIELD_SEC_PARAM = "sec_param"
    CONFIG_FIELD_INT_PRECISION = "integer_precision"
    CONFIG_FIELD_FRAC_PRECISION = "fractional_precision"
    CONFIG_FIELD_MULT_DEPTH = "multiplication_depth"
    CONFIG_FIELD_NUM_SLOTS = "num_slots"
    DEFAULT_CONFIG = {
        CONFIG_FIELD_SEC_PARAM: int(128),
        CONFIG_FIELD_INT_PRECISION: int(10),
        CONFIG_FIELD_FRAC_PRECISION: int(29),
        CONFIG_FIELD_MULT_DEPTH: int(1),
        CONFIG_FIELD_NUM_SLOTS: int(2048)
    }

    def __init__(self, config = None):
        super(CryptoHeLy, self).__init__(config)
        if config is None:
            config = CryptoHeLy.DEFAULT_CONFIG
        elif CryptoHeLy.CONFIG_FIELD_SEC_PARAM not in config or \
            CryptoHeLy.CONFIG_FIELD_INT_PRECISION not in config or \
            CryptoHeLy.CONFIG_FIELD_FRAC_PRECISION not in config or \
            CryptoHeLy.CONFIG_FIELD_MULT_DEPTH not in config or \
            CryptoHeLy.CONFIG_FIELD_NUM_SLOTS not in config:
            raise KeyDistributionInputException("Incomplete config=" + repr(config))
        self.sec_param = config[CryptoHeLy.CONFIG_FIELD_SEC_PARAM]
        self.integer_precision = config[CryptoHeLy.CONFIG_FIELD_INT_PRECISION]
        self.fractional_precision = config[CryptoHeLy.CONFIG_FIELD_FRAC_PRECISION]
        self.multiplication_depth = config[CryptoHeLy.CONFIG_FIELD_MULT_DEPTH]
        self.num_slots = config[CryptoHeLy.CONFIG_FIELD_NUM_SLOTS]
        self.context = None
        self.buffer_ctx = None
        self.buffer_sk = None

    def generate_keys(self):
        requirement = pyhe.HeConfigRequirement(
            num_slots = self.num_slots,
            multiplication_depth = self.multiplication_depth,
            fractional_part_precision = self.fractional_precision,
            integer_part_precision = self.integer_precision,
            security_level = self.sec_param)
        self.context = pyhe.DefaultContext()
        self.context.init(requirement)
        self.buffer_ctx = self.context.save_to_buffer()
        self.buffer_sk = self.context.save_secret_key()

    def get_public_key(self):
        if self.buffer_ctx is None:
            raise KeyDistributionInputException("self.buffer_ctx is None")
        return self.buffer_ctx

    def get_private_key(self):
        if self.buffer_sk is None:
            raise KeyDistributionInputException("self.buffer_sk is None")
        return self.buffer_sk
